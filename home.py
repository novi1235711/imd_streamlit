import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import calendar
from pytz import timezone

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'duty-387503-69ca976b8f4f.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = '1-Jym3yoFFhcEpfiEwwb7i8rXqtLKmbr7011_l5dEqzg'
NL_SHEET_KEY = '1IhGgM9BWXKxO_z0hQvMTkH6-b9Q0_x8wD68nFkcevpI'
sh = gc.open_by_key(SP_SHEET_KEY)
nl = gc.open_by_key(NL_SHEET_KEY)
HD_NAME = 'holidays'
NL_NAME = 'namelist'
A2nd_NAME = 'A_2nd'
hds = sh.worksheet(HD_NAME)
names = nl.worksheet(NL_NAME)
A2nd = sh.worksheet(A2nd_NAME)
holidayslist = hds.get_all_values()
namelist = names.get_all_values()
A2ndlist = A2nd.get_all_values()
df_names = pd.DataFrame(namelist[1:],columns=namelist[0])
df_holidays = pd.DataFrame(holidayslist[1:],columns=holidayslist[0])
df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
hds_arr =  holidayslist[1:]
namelist2 = df_names['内科医師']
timelist2 = df_A2nd['Time']
dtnow = datetime.datetime.now()
now = dtnow.astimezone(timezone('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')
year = int(dtnow.strftime('%Y'))
month = int(dtnow.strftime('%m'))+1
if month == 13:
    year = year+1
    month = 1
namelist_link = '[医師名簿](https://docs.google.com/spreadsheets/d/1IhGgM9BWXKxO_z0hQvMTkH6-b9Q0_x8wD68nFkcevpI/edit#gid=1387675448)'
Table2_link = '[振り分け表](https://docs.google.com/spreadsheets/d/1R5apCzJIKEetmKlEodTpAT8Z2sNdA5lBZcg-ApgVf14/edit#gid=58770345)'

def page_home():
    st.title('Home')
    """
    ##### 回答フォームは左上のメニューから該当のフォームで回答してください。
    ##### (スマホで回答する方は少し上にスクロールして出てくる＞をタップして)
    #### ＊くれぐれも、他人の名前で回答しないようにお願いします。
    #####
    ##### 日当直決め担当者は以下の要領で行ってください。
    ##### 1．左上のメニューから管理者ページにアクセスし、祝日の登録、名簿の確認を行って下さい。
    ##### 2．下記のリンクから振り分け表にアクセスし、表を完成させてください。
    """
    st.markdown(Table2_link, unsafe_allow_html=True)
    """
    ### ＊回答状況＊
    """
    st.write("間違いや再回答をした場合は、以下の履歴を参考に回答を削除してください。")
    st.write("＊トラブル回避のため自動的な上書きはされません。また、1つずつしか削除できないようにしています。")
    df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
    with st.form("delete2"):
        st.write(df_A2nd)
        id2 = st.selectbox("注意して、削除したい回答の時間を選択してください。",timelist2)
        deleted = st.form_submit_button("Delete")
        if deleted:
            df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
            df_A2nd = df_A2nd[df_A2nd['Time']!=id2]
            A2nd.clear()
            set_with_dataframe(A2nd,df_A2nd,row=1,col=1)
            st.write("選択したデータを削除しました。")
            st.write("＊もう一度削除する際は、必ずページを再読み込みしてください。")
            st.write(df_A2nd)
        

def page_form2():
    st.title('日当直回答フォーム')
    """
    ###### ＊NGの日を基準に振り分けるシステムですが、どうしても特定の日でないと日当直が難しい場合はその旨をコメントに記載した上で希望日をご入力ください。
    
    """
    with st.form("my_form"):
        cal = calendar.Calendar().itermonthdays2(year,month)
        cal_arr = list(cal)
        new_cal_arr = []
        new_hds_arr = []
        new_std_arr = []
        for x in cal_arr:
            if x[0] == 0:
                del x
            else:
                if x[1] == 0:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (月)")
                elif x[1] == 1:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (火)")
                elif x[1] == 2:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (水)")
                elif x[1] == 3:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (木)")
                elif x[1] == 4:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (金)")
                elif x[1] == 5:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (土)")
                elif x[1] == 6:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (日)")
        for y in cal_arr:
            if y[0] == 0:
                del y
            else:
                if y[1] == 5:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (土)")
                elif y[1] == 6:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (日)")
                else:
                    del y
        for z in hds_arr:
            new_hds_arr.append(str(z[0]))
        for w in cal_arr:
            if w[0] == 0:
                del w
            else:
                if w[1] == 0:
                    new_std_arr.append(str(year)+"/"+str(month)+"/"+str(w[0])+" (月)")
                elif w[1] == 1:
                    new_std_arr.append(str(year)+"/"+str(month)+"/"+str(w[0])+" (火)")
                elif w[1] == 2:
                    new_std_arr.append(str(year)+"/"+str(month)+"/"+str(w[0])+" (水)")
                elif w[1] == 3:
                    new_std_arr.append(str(year)+"/"+str(month)+"/"+str(w[0])+" (木)")
                elif w[1] == 4:
                    new_std_arr.append(str(year)+"/"+str(month)+"/"+str(w[0])+" (金)")
                else:
                    del w
        
        yourname = st.selectbox(
            'あなたの名前を選んでください',
            namelist2
            )

        comment = st.text_input(
            'ご要望等あればご記載ください。'
        )
        
        NG_list1 = st.multiselect("当直がNGの日を入力ください",new_cal_arr)
        NG_list2 = st.multiselect("日直がNGの日を入力ください",new_hds_arr)

        NG_list3 = st.multiselect("午前がNGの日を入力ください",new_std_arr)
        NG_list4 = st.multiselect("午後がNGの日を入力ください",new_std_arr)

        demandsA2 = st.multiselect("当直の希望日があれば入力ください（参考程度です）",new_cal_arr)
        demandsB2 = st.multiselect("日直の希望日があれば入力ください（参考程度です）",new_hds_arr)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Time: ", now)
            st.write("Name: ", yourname)
            st.write('Your comment: ', comment)
            st.write('You selected: ', NG_list1, NG_list2, NG_list3, NG_list4)
            st.write("上記の内容で提出しました")
            df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
            data2 = [[now,yourname,comment,NG_list1,NG_list2,demandsA2,demandsB2,NG_list3,NG_list4]]
            columns2 = ['Time','Name','Comment','NG1','NG2','OK1','OK2','NG3','NG4']
            nd = pd.DataFrame(data=data2,columns=columns2)
            df_A2nd = pd.concat([df_A2nd,nd],axis=0,)
            set_with_dataframe(A2nd,df_A2nd,row=1,col=1)
            st.write(df_A2nd)

def page_manager():
    st.title('管理者ページ')
    cal = calendar.Calendar().itermonthdays2(year,month)
    cal_arr = list(cal)
    new_cal_arr = []
    for x in cal_arr:
        if x[0] == 0:
            del x
        else:
            if x[1] == 0:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (月)")
            elif x[1] == 1:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (火)")
            elif x[1] == 2:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (水)")
            elif x[1] == 3:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (木)")
            elif x[1] == 4:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (金)")
            elif x[1] == 5:
                del x
            elif x[1] == 6:
                del x
    
    with st.form("holidays"):
        newholidays = st.multiselect(
            '土日を除いた祝日を選んでください。Submitを忘れずに。*祝日のない月であっても、空欄でSubmitしてください。',
            new_cal_arr
        )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("祝日: ", newholidays, "として登録しました。")
            df_holidays = pd.DataFrame({'holidays':newholidays})
            hds.clear()
            set_with_dataframe(hds,df_holidays,row=1,col=1)
            
            st.write(df_holidays)


    "名簿を確認して、編集が必要であれば以下のリンクからGoogleSheetを編集してください。"
    st.dataframe(df_names)
    st.markdown(namelist_link, unsafe_allow_html=True)


selected_page = st.sidebar.radio(
    "メニュー", 
    ["HOME", 
    "回答フォーム", "管理者ページ"
     ]
    )

if selected_page == "HOME":
    page_home()
elif selected_page == "回答フォーム":
    page_form2()
elif selected_page == "管理者ページ":
    page_manager()
else:
    pass




