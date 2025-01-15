# import mysql.connector
# from django.core.management.base import BaseCommand
# from group1.models import PersianWord

# class Command(BaseCommand):
#     help = 'Import words from the cloud MySQL database into the local Django database'

#     def handle(self, *args, **kwargs):
#         # Cloud database connection details
#         db_config = {
#             'host': 'mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com',
#             'port': 11741,
#             'user': 'avnadmin',
#             'password': 'AVNS_QXs1v9qBTveDtLIXZfW',
#             'database': 'defaultdb',
#         }

#         try:
#             # Connect to the cloud database
#             cloud_connection = mysql.connector.connect(**db_config)
#             cursor = cloud_connection.cursor(dictionary=True)

#             # Query the Persian words
#             cursor.execute("SELECT word, frequency FROM group1_persianword")
#             words = cursor.fetchall()

#             # Import words into the local database
#             for word_data in words:
#                 PersianWord.objects.update_or_create(
#                     word=word_data['word'],
#                     defaults={'frequency': word_data['frequency']}
#                 )

#             self.stdout.write(self.style.SUCCESS('Successfully imported words from the cloud database.'))
#         except mysql.connector.Error as e:
#             self.stderr.write(self.style.ERROR(f'Error connecting to the cloud database: {e}'))
#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'cloud_connection' in locals():
#                 cloud_connection.close()



# group1/management/commands/import_words.py
# import os
# from django.core.management.base import BaseCommand
# from group1.models import PersianWord

# class Command(BaseCommand):
#     help = 'Import words from a .txt file to the PersianWord model'

#     def handle(self, *args, **kwargs):
#         file_path = 'C:/Users/Arian/OneDrive/Desktop/distinct_words.txt'
#         if not os.path.exists(file_path):
#             self.stdout.write(self.style.ERROR(f"File {file_path} does not exist"))
#             return

#         with open(file_path, 'r', encoding='utf-8') as file:
#             words = file.readlines()

#         for word in words:
#             word = word.strip()
#             if word:
                
#                 if not PersianWord.objects.filter(word=word).exists():
                    
#                     PersianWord.objects.create(word=word, frequency=0)

#         self.stdout.write(self.style.SUCCESS(f"Successfully imported words from {file_path}"))
