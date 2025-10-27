from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os

from uuid import uuid4
from pathlib import Path


import logging
logger = logging.getLogger(__name__)
# /api/files.py
'''Загрузка файла'''
