import json,re,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open(sys.argv[1],encoding='utf-8'))
L={j['id']:j for j in d['list']}
K=[ # (canonical, group, regex)
("C/C++","언어",r"(?<![A-Za-z#])C\s*/\s*C\+\+|C\+\+|(?<![A-Za-z#/])C\s*(언어|language|기반|프로그래밍|programming)|(?<![A-Za-z])C,\s*C\+\+|임베디드\s*C|Embedded\s*C\b"),
("Python","언어",r"python|파이썬"),
("Rust","언어",r"\brust\b"),
("C#/.NET","언어",r"C#|\.NET"),
("Java/Kotlin","언어",r"\bjava\b|kotlin"),
("Verilog/VHDL","언어",r"verilog|vhdl|systemverilog|\bHDL\b"),
("MATLAB/Simulink","언어",r"matlab|simulink"),
("Shell/스크립트","언어",r"shell|bash|스크립트|script"),
("Linux","OS·플랫폼",r"linux|리눅스"),
("Linux 커널/드라이버","OS·플랫폼",r"kernel|커널|device\s*driver|디바이스\s*드라이버|드라이버"),
("RTOS","OS·플랫폼",r"rtos|freertos|zephyr|threadx|vxworks|실시간\s*(운영|OS)"),
("Yocto/Buildroot","OS·플랫폼",r"yocto|buildroot|bitbake"),
("BSP/부트로더","OS·플랫폼",r"\bBSP\b|bootloader|부트로더|u-boot|uboot"),
("Android","OS·플랫폼",r"android|안드로이드|AOSP|HAL\b"),
("ROS","OS·플랫폼",r"\bROS2?\b"),
("AUTOSAR","OS·플랫폼",r"autosar"),
("Qt","OS·플랫폼",r"\bQt\b|QML"),
("MCU","프로세서",r"\bMCU|마이크로컨트롤러|micro\s*controller|펌웨어|firmware"),
("ARM/Cortex","프로세서",r"\bARM\b|cortex"),
("STM32/nRF 등","프로세서",r"stm32|nrf5|esp32|nxp|renesas|infineon"),
("FPGA","프로세서",r"fpga|xilinx|altera|vivado|zynq"),
("SoC/AP","프로세서",r"\bSoC|\bAP\b|qualcomm|퀄컴|exynos"),
("DSP/신호처리","프로세서",r"\bDSP\b|신호\s*처리|signal\s*processing"),
("GPU/CUDA·NPU","프로세서",r"cuda|gpu|npu|jetson|tensorrt"),
("UART/SPI/I2C","통신·인터페이스",r"uart|\bspi\b|i2c|i²c|gpio"),
("CAN/차량통신","통신·인터페이스",r"\bCAN\b|CAN-FD|CANFD|LIN\b|flexray|차량\s*네트워크|automotive\s*ethernet"),
("Ethernet/TCP-IP","통신·인터페이스",r"ethernet|이더넷|tcp|socket|소켓|네트워크\s*프로그래밍"),
("USB/PCIe 고속IF","통신·인터페이스",r"\bUSB|pcie|pci\s*express|mipi|ddr|고속\s*(신호|인터페이스)|high-speed|serdes|hdmi"),
("BLE/Wi-Fi/무선","통신·인터페이스",r"\bBLE\b|bluetooth|블루투스|wi-?fi|zigbee|lora|lte|5G|무선|wireless|RF\b|uwb|gnss|gps"),
("Modbus/산업통신","통신·인터페이스",r"modbus|ethercat|profinet|plc|opc"),
("MQTT/IoT","통신·인터페이스",r"mqtt|\bIoT\b"),
("회로설계","HW 설계",r"회로\s*설계|회로\s*개발|schematic|회로도|circuit"),
("PCB/Artwork","HW 설계",r"pcb|artwork|아트웍|layout"),
("OrCAD/Altium/PADS","HW 설계",r"orcad|altium|pads|cadence|allegro|kicad|EDA"),
("아날로그/전원회로","HW 설계",r"아날로그|analog|전원\s*(회로|설계)|power\s*(supply|electronics|design)|전력\s*(전자|변환)|DC-?DC|인버터|컨버터|SMPS|BMS|배터리"),
("모터제어","HW 설계",r"모터|motor|bldc|servo|서보"),
("센서/계측","HW 설계",r"센서|sensor|imu|lidar|라이다|카메라|camera|이미지\s*센서"),
("EMC/인증","HW 설계",r"emc|emi|\bKC\b|\bCE\b|FCC|인증|ESD"),
("시뮬레이션(SPICE 등)","HW 설계",r"spice|simulation|시뮬레이션|SI/PI|signal\s*integrity|HFSS|ADS\b"),
("반도체/ASIC","HW 설계",r"반도체|asic|rtl|칩\s*설계|post-silicon|validation|웨이퍼"),
("계측장비(오실로 등)","도구",r"오실로|oscilloscope|로직\s*분석기|logic\s*analyzer|스펙트럼|계측\s*장비|측정\s*장비|JTAG|디버거|debugger"),
("Git/형상관리","도구",r"\bgit\b|github|gitlab|svn|형상\s*관리|version\s*control"),
("CI/CD·Docker","도구",r"ci/cd|jenkins|docker|kubernetes"),
("테스트/검증 자동화","도구",r"테스트\s*자동화|test\s*automation|unit\s*test|단위\s*테스트|HILS|SILS|HIL\b|검증"),
("ISO 26262/ASPICE","도구",r"26262|aspice|기능\s*안전|functional\s*safety|misra|21434"),
("딥러닝/AI","도메인",r"딥러닝|deep\s*learning|머신\s*러닝|machine\s*learning|\bAI\b|인공지능|LLM|pytorch|tensorflow|onnx"),
("영상/비전","도메인",r"영상|비전|vision|opencv|isp\b|이미지\s*처리"),
("로봇/제어","도메인",r"로봇|robot|제어\s*(이론|알고리즘|기|시스템)|control|PID|매니퓰레이터|자율\s*주행"),
("자동차/모빌리티","도메인",r"자동차|차량|automotive|모빌리티|mobility|ECU|전장|IVI"),
("보안","도메인",r"보안|security|암호|crypto|secure\s*boot|TEE"),
("양산/제품화","도메인",r"양산|mass\s*production|제품화|시제품|prototype"),
("데이터시트/HW 이해","기본 역량",r"datasheet|데이터\s*시트|하드웨어\s*(에\s*대한\s*)?(이해|지식)|회로\s*이해|회로도\s*(해석|이해)"),
("CS 기초(자료구조/OS)","기본 역량",r"자료\s*구조|알고리즘|운영\s*체제|operating\s*system|컴퓨터\s*구조|CS\s*(기초|지식)|data\s*structure"),
("영어","기본 역량",r"영어|english|영문|외국어|business\s*level|TOEIC|OPIc"),
("문서화/커뮤니케이션","기본 역량",r"문서|커뮤니케이션|communication|협업|소통"),
("운전 가능","기본 역량",r"운전\s*(가능|면허)|면허\s*소지"),
]
KC=[(n,g,re.compile(p,re.I)) for n,g,p in K]
def kws(t): return [n for n,g,r in KC if r.search(t or "")]
def degree(t):
    t=t or ""
    if re.search(r"박사|ph\.?d",t,re.I): return "박사"
    if re.search(r"석사|master",t,re.I): return "석사 이상"
    if re.search(r"학사|대졸|대학교\s*졸업|4년제|bachelor|BS\b|B\.S",t,re.I): return "학사 이상"
    if re.search(r"전문\s*학사|초대졸|2년제",t,re.I): return "초대졸 이상"
    if re.search(r"전공",t): return "관련 전공(학위 미명시)"
    return "명시 없음"
rows=[]
for j in d['detail']:
    if not j: continue
    l=L[j['id']]; dt=j['detail']
    cats={c['id'] for c in j['category_tags']}
    role="임베디드+하드웨어" if {658,672}<=cats else ("임베디드" if 658 in cats else "하드웨어")
    a,b=l.get('annual_from',0),l.get('annual_to',100)
    band = "신입 가능" if a==0 else "1~2년" if a<=2 else "3~4년" if a<=4 else "5~6년" if a<=6 else "7년 이상"
    req,pref=dt.get('requirements',''),dt.get('preferred_points','')
    ad=j.get('address') or l.get('address') or {}
    rows.append(dict(id=j['id'],url=f"https://www.wanted.co.kr/wd/{j['id']}",company=j['company']['name'],
      industry=j['company'].get('industry_name') or "",position=j['position'],role=role,
      location=ad.get('location') or "기타",district=ad.get('district') or "",
      exp_min=a,exp_max=b,exp_band=band,due=(j.get('due_time') or "상시"),
      degree_req=degree(req),req_kw="|".join(kws(req)),pref_kw="|".join(kws(pref)),
      skill_tags="|".join(s['title'] for s in j.get('skill_tags',[])),
      requirements=req.strip(),preferred=pref.strip(),main_tasks=(dt.get('main_tasks') or '').strip()))
json.dump(rows,open("jobs.json","w",encoding="utf-8"),ensure_ascii=False)
json.dump([dict(keyword=n,group=g) for n,g,_ in K],open("kwgroups.json","w",encoding="utf-8"),ensure_ascii=False)
import os;print(len(rows),os.path.getsize("jobs.json"))
c=collections.Counter(k for r in rows for k in r['req_kw'].split('|') if k);print(c.most_common(40))
p=collections.Counter(k for r in rows for k in r['pref_kw'].split('|') if k);print(p.most_common(25))
print(collections.Counter(r['role'] for r in rows),collections.Counter(r['exp_band'] for r in rows),collections.Counter(r['degree_req'] for r in rows),collections.Counter(r['location'] for r in rows).most_common(8))
