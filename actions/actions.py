# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from unidecode import unidecode
from rasa_sdk.events import EventType, SlotSet
import requests
from email.mime.text import MIMEText
import json
import smtplib
from email.mime.multipart import MIMEMultipart



class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:

        SendEmail(
            tracker.get_slot("email"),tracker.get_slot("message")
        )

        dispatcher.utter_message("Cảm ơn bạn đã gửi câu hỏi cho tổ tư vấn, các thầy cô sẽ xem xét và trả lời câu hỏi của bạn sớm nhất có thể.")
        return []

def SendEmail(email,message):
    fromaddr = 'dslabneu@gmail.com'
    msg = MIMEMultipart()
    toaddr = 'dslabneu@gmail.com'

    msg['To'] = "dslabneu@gmail.com"
    msg['Subject'] = "NEU - QUESTION FROM" + email
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    try:
       # password here
        s.login(fromaddr, "dslabneu123")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
    except:
        print("Error")
    finally:
        s.quit()

def login():
    url = 'https://writing9.com/api/login'
    myobj = {'email': 'trung.ntt1210@gmail.com', 'password':'dslabneu'}


    x = requests.post(url, data = myobj)
    token = x.json()
    return token['token']


def get_score(text, question):
    try:
     url = 'https://writing9.com/api/save'
     myobj = {'text': str(text), 'question': str(question)}
     token = login()
     authorization = "Bearer " + token
     headers = {
                'authorization': authorization,
                'content-type' : 'application/json',
                'Accept': 'text/plain'
                }
     x = requests.post(url, data = json.dumps(myobj), headers= headers)
     return x.json()['text']['_id']
    except:
     return "error"

class ActionIelts(Action):
    def name(self) -> Text:
        return "action_ielts_api"
    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:

        question = tracker.get_slot("question")
        text = tracker.get_slot("text")
        token = get_score(text, question)
        if token == "error":
         dispatcher.utter_message("Hệ thống chấm điểm bị lỗi, vui lòng bạn thử lại lúc khác nhé :(")   
        else:    
         dispatcher.utter_message("Điểm IELTS của bạn: https://writing9.com/text/"+token)
        return[]

class ActionGreetNewUser(Action):
    """Return greet with name"""

    def name(self) -> Text:
        return "action_greet_api"

    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.current_state()['sender_id']
        print(sender_id)
        page_access_token = 'EAALWDFPUBTwBAO1PQv5Kwa5r8htdZARbCeONDlbgf0rcIqu3VEQPk6tZBM5wQRZAv38jaDTfbzWR8BHAFgCv3RVeFFfjTtRi0DbwXdnef2t7ylU85xYYUqcjRdkw6tG1BWMda9UPLoP4MhiqANrx4mN8DJb0cCFiWX18ZCQO9MJKn41xsbDC'
        res = requests.get('https://graph.facebook.com/{}?fields=name,first_name,last_name,profile_pic&access_token={}'.format(
                    sender_id, page_access_token))
        #res = requests.get("https://graph.facebook.com/v10.0/"+sender_id+"?access_token="+page_access_token)
        data = res.json()
        fbname = data["name"]
        dispatcher.utter_message(template = "utter_greet_api", name = fbname)

        return []

class MajorSpecifier(Action):

    def name(self) -> Text:
        return 'action_major_specifier'

    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mfe = ["isfa","lyon","act","actuary","dinh phi bao hiem","quan tri rui ro","actuarial","ep02","lyon","epo2","isfa","actuaries", "toan tai chinh",
                "toan kt","toan kinh te","tkt", "data","data science","khoa hoc du lieu","ds","khdl","cntt","du lieu", "machine" ,"datascience","ep03","dseb","desb","dbse","epo3","science"]
        tai_chinh_ngan_hang =['tai chinh ngan hang', 'tcnh', 'dau tu tai chinh','tai chinh doanh nghiep',
                'tai chinh cong', 'nganh ngan hang', 'dau tu tai chinh','bfi','chuong trinh cong nghe tai chinh','bft', "cong nghe tai chinh"]
        bat_dong_san = ['khoa bat dong san va kinh te tai nguyen','bat dong san', 'kinh te tai nguyen',
                'bat dong san va kinh te tai nguyen', 'bat dong san', 'kinh te nong nghiep', "nong nghiep",
                'kinh te tai nguyen', 'quan ly dat dai']
        bao_hiem = ['bao hiem', 'khoa bao hiem']
        dau_tu = ['quan tri khach san', 'quan tri dich vu du lich va lu hanh', 'chuong trinh quan tri khach san quoc te',
                    'khoa dau tu', 'quan tri khach san quoc te', "quan ly du an", "dau tu"]
        ke_kiem = ['ke toan', 'kiem toan', 'ke toan tich hop chung chi quoc te - act-icaew',
            'kiem toan tich hop chung chi quoc te - aud-icaew', 'act', 'aud', 'icaew', "ke kiem"]
        ke_hoach_phat_trien = ['ke hoach va phat trien', 'kinh te phat trien']
        kinh_te_hoc = ['khoa kinh te hoc', 'kinh te hoc tai chinh', 'fe','kinh te hoc', "kth", "kthtc", "kinh te", "lincoln-neu", "lincoln"]
        quan_ly_nhan_luc = ['kinh te va quan ly nguon nhan luc', 'kinh te (chuyen nganh kinh te va quan ly nguon nhan luc)', 
                        'quan tri nhan luc', 'quan ly nguon nhan luc']
        khoa_hoc_quan_ly = ['khoa hoc quan ly', 'quan ly cong','quan ly cong va chinh sach', 'epmp']
        luat = ['luat', 'khoa luat', 'luat kinh te']
        marketing = ['marketing', 'quan he cong chung', 'quan he', 'tham dinh gia']
        tai_nguyen_moi_truong = ['moi truong, bien doi khi hau va do thi', 'quan ly tai nguyen va moi truong', 'quan ly do thi', 'tai nguyen', 'moi truong', 'kinh te va quan ly do thi', "kinh te tai nguyen thien nhien", "tai nguyen thien nhien"]
        ngoai_ngu_kinh_te = ["ngoai ngu kinh te", 'ngon ngu anh', "ngon ngu"]
        quan_tri_kinh_doanh = ['quan tri dieu hanh thong minh','e-som', 'esom','quan tri chat luong va doi moi','emqi','quan tri kinh doanh', "kinh doanh so", "e-bdb", "ebdb"]
        thong_ke = ["thong ke", 'thong ke kinh te']
        thuong_mai_kinh_te_quoc_te = ["kinh te quoc te", 'kinh doanh quoc te','kinh doanh thuong mai', 'thuong mai dien tu','logistics va quan ly chuoi cung ung','lsic','thuong mai va kinh te quoc te', 'logistic', "thuong mai quoc te", "thuong mai"]
        cntt = ["cong nghe thong tin va kinh te so", 'cong nghe thong tin','khoa hoc may tinh','he thong thong tin quan ly','cntt','khmt', "he thong thong tin"]
        dao_tao_quoc_te = ["dao tao quoc te", "bbae", "khoi nghiep", "phat trien kinh doanh", "khoa quoc te"]
        pohe = ["pohe", "phan tich kinh doanh", "dinh huong ung dung", "business analysis"]
        du_lich = ["quan tri dich vu du lich", "lu hanh", "quan tri khach san", "quan tri khach san quoc te", "ihme"]
        lien_thong = ["lien thong", "dai hoc tai chuc", 'tai chuc', 'trung cap']
        dao_tao_tu_xa = ['dao tao tu xa']
        time = ['khi nao', 'bao gio', 'han cuoi', 'han chot', 'thoi gian' , 'bat dau tu']
        hoc_phi = ['hoc phi', 'chi phi']
        phuong_thuc = ['phuong thuc xet tuyen ket hop', 'phuong thuc xtkh', 'phuong thuc xet tuyen', 'xtkh', 'thong tin chi tiet ve']
        xtkh = ['xet tuyen ket hop', "link", "ho so online"]
        online = ['diem gia dinh', "khong dung dinh dang", "error 403", "error"]
        giay_to = ['cmnd','cccd', 'the can cuoc', 'chung minh thu', 'giay to', 'ban sao', 'ban cong chung', "ban goc", 'giay xac nhan', 'ban chinh', 'hoc ba', 'file pdf', 'giay chung nhan']
        le_phi = ['le phi xet tuyen', 'le phi', 'bien lai', 'chuyen khoan']
        sbd = ['sbd', 'so bao danh']
        http = ['https']
        bong_da = ['bong da', 'neu league']
        error = ['quen mat khau', 'phat hien sai', 'thay sai', 'ghi nham', 'quen mat mat khau', 'nhap nham', 'khong chinh xac', 'chua xac nhan', 'chua duoc xac nhan', 'khong dien duoc', 'khong tim thay', 'k tim thay', 'khong bam duoc', 'chua cho nhap','dien sai','viet sai', 'bi sai', 'bao loi', 'bi loi', 'gap loi' 'sai', 'ghi thieu', 'sua lai', 'khong dung', 'dien nham', 'khac phuc', 'email', 'gmail', 'mat khau', 'mail', 'sai sot']
        thoi_gian = ['nam ngoai', 'cac nam truoc', '2018', '2019', '2017', '20']    
        name = ['dat ten']   

        id_user = tracker.sender_id
        f = open("user_database.txt", "a")
        f.write(id_user+"\n")
        f.close()


        user_input = unidecode(tracker.latest_message.get('text')).lower()
        print(user_input)
        intent = tracker.latest_message['intent'].get('name')
        ogintent = intent
        if any(map(user_input.__contains__, error)):
           intent = "utter_error_occur"
        elif any(map(user_input.__contains__, name)):
           intent = "utter_giay_to"
        elif any(map(user_input.__contains__, sbd)):
           intent = "utter_sbd"
        elif any(map(user_input.__contains__, mfe)):
           intent = "utter_switch_mfe"
        elif any(map(user_input.__contains__, tai_chinh_ngan_hang)):
           intent = "utter_switch_tai_chinh_ngan_hang"
        elif any(map(user_input.__contains__, pohe)):
           intent = "utter_switch_pohe"
        elif any(map(user_input.__contains__, dao_tao_quoc_te)):
           intent = "utter_switch_dao_tao_quoc_te"
        elif any(map(user_input.__contains__, bat_dong_san)):
           intent = "utter_switch_bat_dong_san"
        elif any(map(user_input.__contains__, du_lich)):
           intent = "utter_switch_du_lich"
        elif any(map(user_input.__contains__, bao_hiem)):
           intent = "utter_switch_bao_hiem"
        elif any(map(user_input.__contains__, dau_tu)):
           intent = "utter_switch_dau_tu"
        elif any(map(user_input.__contains__, ke_kiem)):
           intent = "utter_switch_ke_kiem"
        elif any(map(user_input.__contains__, ke_hoach_phat_trien)):
           intent = "utter_switch_ke_hoach_phat_trien"
        elif any(map(user_input.__contains__, quan_ly_nhan_luc)):
           intent = "utter_switch_quan_ly_nhan_luc"
        elif any(map(user_input.__contains__, khoa_hoc_quan_ly)):
           intent = "utter_switch_khoa_hoc_quan_ly"
        elif any(map(user_input.__contains__, luat)):
           intent = "utter_switch_luat"
        elif any(map(user_input.__contains__, marketing)):
           intent = "utter_switch_marketing"
        elif any(map(user_input.__contains__, tai_nguyen_moi_truong)):
           intent = "utter_switch_tai_nguyen_moi_truong"
        elif any(map(user_input.__contains__, ngoai_ngu_kinh_te)):
           intent = "utter_switch_ngoai_ngu_kinh_te"
        elif any(map(user_input.__contains__, quan_tri_kinh_doanh)):
           intent = "utter_switch_quan_tri_kinh_doanh"
        elif any(map(user_input.__contains__, thuong_mai_kinh_te_quoc_te)):
           intent = "utter_switch_thuong_mai_kinh_te_quoc_te"
        elif any(map(user_input.__contains__, cntt)):
           intent = "utter_switch_cntt"
        elif any(map(user_input.__contains__, thong_ke)):
           intent = "utter_switch_thong_ke"
        elif any(map(user_input.__contains__, kinh_te_hoc)):
           intent = "utter_switch_kinh_te_hoc"
        elif any(map(user_input.__contains__, lien_thong)):
           intent = "utter_switch_lien_thong"
        elif any(map(user_input.__contains__, dao_tao_tu_xa)):
           intent = "utter_switch_dao_tao_tu_xa"
        elif any(map(user_input.__contains__, time)):
           intent = "utter_time"
        elif any(map(user_input.__contains__, hoc_phi)):
           intent = "utter_hoc_phi"
        elif any(map(user_input.__contains__, online)):
           intent = "utter_online"
        elif any(map(user_input.__contains__, le_phi)):
           intent = "utter_le_phi_xet_tuyen"
        elif any(map(user_input.__contains__, giay_to)):
           intent = "utter_giay_to"
        elif any(map(user_input.__contains__, phuong_thuc)):
           intent = "utter_phuong_thuc_xet_tuyen_ket_hop"
        elif any(map(user_input.__contains__, xtkh)):
           intent = "utter_nguyen_tac_xet_tuyen_ket_hop"
        elif any(map(user_input.__contains__, http)):
           intent = "utter_emotes"
        elif any(map(user_input.__contains__, bong_da)):
           intent = "utter_bong_da"
        elif len(user_input) < 2:
           intent = "utter_greet"
        else :
           intent = "utter_" + ogintent
        if(user_input.find('https') != -1):
           intent = "utter_emotes"
        if(intent == 'utter_diem_chuan' and any(map(user_input.__contains__, thoi_gian))):
           intent = 'utter_loai_to_hop_xet_tuyen'
        print(tracker.latest_message)   
        print(intent)
        try:
         dispatcher.utter_message(template=intent)
        except:
         dispatcher.utter_message(template="utter_"+ogintent)
        return []