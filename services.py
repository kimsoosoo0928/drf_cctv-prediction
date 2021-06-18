from rest_framework.common.entity import FileDTO
from rest_framework.common.services import Reader, Printer
import pandas as pd
import numpy as np
'''
살인 발생,살인 검거,강도 발생,강도 검거,강간 발생,강간 검거,절도 발생,절도 검거
'''
class Service(Reader):

    def __init__(self):
        self.f = FileDTO()
        self.r = Reader()
        self.p = Printer()

        self.crime_reate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인','강도','강간','철도','폭력']

    def save_police_pos(self):
        f = self.f
        r = self.r
        p = self.p
        f.context = './data/'
        f.fname = 'crime_in_seoul'
        crime = r.csv(f)
        # p.dframe(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울'+str(name[:-1]+'경찰서'))
            station_addrs = []
            station_lats = []
            station_lngs = []
            gmaps = r.gmaps()
            for name in station_names:
                t = gmaps.geocode(name, language='ko')
                station_addrs.append(t[0].get('formatted_address'))
                t_loc = t[0].get('geometry')
                station_lats.append(t_loc['location']['lat'])
                station_lngs.append(t_loc['location']['lng'])
                # print(f'name{t[0].get("formatted_address")}')
            gu_names = []
            for name in station_addrs:
                t = name.split()
                gu_name = [gu for gu in t if gu[-1] == '구'][0]
                gu_names.append(gu_name)
            crime['구별'] = gu_names
            # 구 와 경찰서의 위치가 다른 경우 수작업
            crime.loc[crime['관서명'] == '혜화서', ['구별']] == '종로구'
            crime.loc[crime['관서명'] == '서부서', ['구별']] == '은평구'
            crime.loc[crime['관서명'] == '강서서', ['구별']] == '양천구'
            crime.loc[crime['관서명'] == '종암서', ['구별']] == '성북구'
            crime.loc[crime['관서명'] == '방배서', ['구별']] == '서초구'
            crime.loc[crime['관서명'] == '수서서', ['구별']] == '강남구'
            crime.to_csv('./saved_data/police_pos.csv')

        def save_cctv_pop(self):
            f = self.f
            r = self.r
            p = self.p
            f.context = './data/'
            f.name = 'cctv_in_seoul'
            cctv = r.csv(f)

            cctv = r.xls(f, 2, 'B, D, G, J, N')
            p.dfname(pop)

            cctv.rename(columns={cctv.columns[0]:'구별'}, inplace=True)

            pop.rename(columns={
                pop.columns[0]:'구별',
                pop.columns[1]: '인구수',
                pop.columns[2]: '한국인',
                pop.columns[3]: '외국인',
                pop.columns[4]: '고령자',
            }, inplace=True)
            print('*' * 100)
            pop.drop([25], inplace=True)
            print(pop)
            pop['외국인비율'] = pop['외국인'].astype(int) / pop['인구수'].astype(int) * 100
            pop['외국인비율'] = pop['고령자'].astype(int) / pop['인구수'].astype(int) * 100

            cctv.drop(['2013년도 이전','2014년', '2015년', '2016년'],1, inplace=True)
            cctv_pop = pd.merge(cctv, pop, on = '구별')
            cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
            cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])

            print(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
                  f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
            """
             고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                         [-0.28078554  1.        ]] 
             외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                         [-0.13607433  1.        ]]
            r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
            r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
            r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
            r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
            r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
            r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
            r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
            고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                        [-0.28078554  1.        ]]
            외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                        [-0.13607433  1.        ]]                        
             """

            cctv_pop.to_csv()









if __name__ == '__main__':
    s = Service()
    # s.save_police_pos()
    s.save_cctv_pos()