import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
from services import Service
class Crime_API(object):

    @staticmethod
    def main():
        crimeService = Service()
        while 1:
            menu = input('0-Exit\n'
                         '1-서울CCTV DF\n'
                         '2-서울범죄 DF\n'
                         '3-경찰서위치 DF\n'
                         '4-실업율 DF\n'
                         '5-엑셀POP')
            if menu =='0':
                break
            elif menu == '1':
                crimeService.csv({'context': './data/', 'fname': 'cctv_in_seoul'})
            elif menu == '2':
                pass
            elif menu == '3':
                pass
            elif menu == '4':
                pass
            elif menu == '5':
                pass
            else:
                continue

Crime_API.main()