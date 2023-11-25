import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Pages

class Command(BaseCommand):
    help = "backup Pages data"

    def handle(self, *args, **options):
        #実行時のYYYYMMDDを取得
        date= datetime.date.today().strftime("%Y%m%d")

        #保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'diary_'+date+'.csv'

        #保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        #バックアップファイルの作成
        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            #ヘッダーの書き込み
            header = [field.name for field in Pages._meta.fields]
            writer.writerow(header)

            #Pagesテーブルの全データを取得
            pages = Pages.objects.all()

            #データ部分の書き込み
            for page in pages:
                writer.writerow([str(page.user),
                                 page.title,
                                 page.content,
                                 str(page.photo1),
                                 str(page.photo2),
                                 str(page.photo3),
                                 str(page.created_at),
                                 str(page.updated_at)])
            #保存ディレクトリのファイルリストを取得
            files = os.listdir(settings.BACKUP_PATH)
            #ファイルが設定数以上あったら一番古いふぁいるを除作
            if len(files) >= settings.NUM_SAVED_BACKUP:
                files.sort()
                os.remove(settings.BACKUP_PATH + files[0])