# largely transplanted from comet-sendvo script:
# https://github.com/jdswinbank/Comet/blob/release-1.0/scripts/comet-sendvo
# Should track updates.

from __future__ import absolute_import
import logging
import subprocess
import voeparse
import tempfile
logger = logging.getLogger(__name__)
def send_voevent(voevent, host='localhost', port=8098):
    tf = tempfile.TemporaryFile()
    voeparse.dump(voevent, tf)
    tf.seek(0)
    # tf.close()
    try:
        cmd = ['comet-sendvo']
        cmd.append('--host=' + host)
        cmd.append('--port=' + str(port))
        subprocess.check_call(cmd, stdin=tf)
    except subprocess.CalledProcessError as e:
        logger.error("send_voevent failed")
        raise e


    
