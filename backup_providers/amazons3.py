#!/usr/bin/python

import os
import sys
import glob
import subprocess
import contextlib
import functools
import multiprocessing
import boto
import traceback
from multiprocessing.pool import IMapIterator

class AmazonS3:
	def __init__(self, keyid, key):
		# Create the connection
		self.conn = boto.connect_s3(keyid, key)
		self.log = "Using Amazon S3\n"
		
	def checkLocation(self, base_dir, backup_type):
		self.base_dir = base_dir
		self.backup_type = backup_type

		# get the bucket.  This API creates the bucket if it doesn't exist, and returns the bucket object if it does.
		self.bucket = self.conn.create_bucket(base_dir + "-pyback")
	
	def rotateBackup (self, maxFiles):
		# Get the current number of objects for this bckup type
		self.log += "Checking for old backups\n"
		priorBackups = self.bucket.list(prefix=self.backup_type)

		archives = []
		for backup in priorBackups:
			archives.append(backup.name)
		currentBackups = len(archives)

		if currentBackups <= maxFiles:
			self.log += "Number of backups (" + str(currentBackups) + ") has not reached the maximum threshold (" + str(maxFiles) + "). Will not remove previous backups.\n"
		else:
			while currentBackups > maxFiles:
				
				# Set the filename to be the first file returned.  Since we're using date-formatted filenames, this works.  Other naming schemes will require adjustment here.
				filename =archives[0]
				filename = str(filename)
				self.log += "Deleting " + filename + "\n"
				
				# Delete the object
				self.bucket.get_key(filename).delete()
				
				currentBackups -= 1
				
	def upload_cb(self, complete, total):
		sys.stdout.write(".")
		sys.stdout.flush()

	def _standard_transfer(self, bucket, s3_key_name, transfer_file, use_rr):
		print " Upload with standard transfer, not multipart."
		new_s3_item = bucket.new_key(s3_key_name)
		new_s3_item.set_contents_from_filename(transfer_file, reduced_redundancy=use_rr,
						      cb=upload_cb, num_cb=10)
		print

	def map_wrap(f):
		@functools.wraps(f)
		def wrapper(*args, **kwargs):
			return apply(f, *args, **kwargs)
		return wrapper

	def mp_from_ids(self, mp_id, mp_keyname, mp_bucketname):
		"""Get the multipart upload from the bucket and multipart IDs.

		This allows us to reconstitute a connection to the upload
		from within multiprocessing functions.
		"""
		conn = self.conn
		bucket = self.bucket
		mp = boto.s3.multipart.MultiPartUpload(bucket)
		mp.key_name = mp_keyname
		mp.id = mp_id
		return mp

	@map_wrap
	def transfer_part(self, instance, mp_id, mp_keyname, mp_bucketname, i, part):
		"""Transfer a part of a multipart upload. Designed to be run in parallel.
		"""
		mp = mp_from_ids(mp_id, mp_keyname, mp_bucketname)
		print " Transferring", i, part
		with open(part) as t_handle:
			mp.upload_part_from_file(t_handle, i+1)
		os.remove(part)
	
	@contextlib.contextmanager
	def multimap(self, cores=None):
		"""Provide multiprocessing imap like function.

		The context manager handles setting up the pool, worked around interrupt issues
		and terminating the pool on completion.
		"""
		if cores is None:
		    cores = max(multiprocessing.cpu_count() - 1, 1)
		def wrapper(func):
		    def wrap(self, timeout=None):
			return func(self, timeout=timeout if timeout is not None else 1e100)
		    return wrap
		IMapIterator.next = wrapper(IMapIterator.next)
		pool = multiprocessing.Pool(cores)
		yield pool.imap
		pool.terminate()

	def _multipart_upload(self, instance, bucket, s3_key_name, tarball, mb_size, use_rr=True):
		"""Upload large files using Amazon's multipart upload functionality.
		"""
		cores = multiprocessing.cpu_count()
		def split_file(in_file, mb_size, split_num=5):
			prefix = os.path.join(os.path.dirname(in_file),
					      "%sS3PART" % (os.path.basename(s3_key_name)))
			split_size = int(min(mb_size / (split_num * 2.0), 250))
			if not os.path.exists("%saa" % prefix):
				cl = ["split", "-b%sm" % split_size, in_file, prefix]
				subprocess.check_call(cl)
			return sorted(glob.glob("%s*" % prefix))

		mp = bucket.initiate_multipart_upload(s3_key_name, reduced_redundancy=use_rr)
		with self.multimap(cores) as pmap:
			for _ in pmap(transfer_part, ((mp.id, mp.key_name, mp.bucket_name, i, part)
						      for (i, part) in
						      enumerate(split_file(tarball, mb_size, cores)))):
			    pass
		mp.complete_upload()
		
	def pushBackup(self, backup_name, backup_file):
		backup_file += "/" + backup_name
		try:
			# Create the backup name to work with the RS Cloud pseudo-directory
			self.backup_name = self.backup_type + "/" + backup_name
		
			self.log += "Creating object for backup file: " + self.backup_name + "\n"
			key = self.bucket.new_key(self.backup_name)
		
			# Upload the backup file to remote storage
			mb_size = os.path.getsize(backup_file) / 1e6
			self.log += "File size:" + str(mb_size) + "Mb\n"
			if mb_size < 60:
			        self.log += "Using standard upload method\n"
				self._standard_transfer(self.bucket, key, backup_file, False)
			else:
			        self.log += "Using multipart upload\n"
				self._multipart_upload(self.bucket, key, backup_file, mb_size, False)
			key.set_acl=('private')
			return "Ok"
		except Exception, e:
			self.log += "There was an error creating the remote backup.\n"
			self.log += str(traceback.format_exc()) + "\n"
			self.log += "Backup file is located at " + backup_file + "\n"
			self.log += "Please move the backup manually\n"
			return "Error"
