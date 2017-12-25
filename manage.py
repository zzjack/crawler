import os
import sys

#everysetting need to check the setting file to verify the setting is production environment.

# Modified_Time: 11.16
# Theme: <1> add zhengxin91 interface;
#        <2> create some new tables in database crawler and boshidun;

# Modified Time: 11.29
# Theme: <1> store emd008 details in database boshidun.
# Note: The program just supports to store emd008 in boshidun.
# If emd008 wants to be stored in ssd,need to add some codes.
# modified file:
#   <1> crawler/app_crawler/storage/huadao/infos.py
#   <2> crawler/app_crawler/storage/huadao/infos_emd008.py
#   <3> crawler/app_crawler/views/helpme.py
#   <4> crawler/app_crawler/models.py
# add table name:
#     boshidun:
#     hd_emd008_manager/hd_emd008_emr002/hd_emd008_emr004/hd_emd008_emr007/hd_emd008_emr009
#     hd_emd008_emr012/hd_emd008_emr013

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "\nDo you start the program with python3?"
                "\nCouldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable?"
                "\nDid you forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
