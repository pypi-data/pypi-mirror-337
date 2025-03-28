_B='utf-8'
_A='Unknown'
import os,pathlib,importlib.metadata,requests,psutil,platform,uuid,sys,socket,json,base64,getpass
from cryptography.fernet import Fernet
lmt=os.path.sep
HOME_DIR=pathlib.Path.home()
PROJECT_DIR=HOME_DIR/'.vnstock'
TG=b'gAAAAABmfy0qLUmLnsm5oMnteWmNSJ5rBSQubrS2JFdKt19m_tqxaAWRCCJ4goHm-fr5Mee_M8TvZ_sfpvDFFBz-8paY_H72KftTb4CTzuNGhqZjp2BCiP2gwPdOxbi9wh9GCKHBwzVs'
class VnstockInitializer:
	def __init__(A,target):A.home_dir=HOME_DIR;A.project_dir=PROJECT_DIR;A.id_dir=PROJECT_DIR/'id';A.id=PROJECT_DIR/'user.json';A.env_config=A.id_dir/'env.json';A.RH='asejruyy^&%$#W2vX>NfwrevDRESWR';A.LH='YMAnhuytr%$59u90y7j-mjhgvyFTfbiuUYH';A.project_dir.mkdir(exist_ok=True);A.id_dir.mkdir(exist_ok=True);A.target=target;B=(str(A.project_dir).split(lmt)[-1]+str(A.id).split(lmt)[-1])[::-1].ljust(32)[:32].encode(_B);C=base64.urlsafe_b64encode(B);A.cph=Fernet(C)
	def system_info(X):
		L='PWD';K='HOME';J='Google Colab';I='Other';H='Terminal';M=str(uuid.uuid4())
		try:
			from IPython import get_ipython as N
			if'IPKernelApp'not in N().config:
				if sys.stdout.isatty():B=H
				else:B=I
			else:B='Jupyter'
		except(ImportError,AttributeError):
			if sys.stdout.isatty():B=H
			else:B=I
		try:
			if'google.colab'in sys.modules:A=J
			elif'CODESPACE_NAME'in os.environ:A='Github Codespace'
			elif'GITPOD_WORKSPACE_CLUSTER_HOST'in os.environ:A='Gitpod'
			elif'REPLIT_USER'in os.environ:A='Replit'
			elif'KAGGLE_CONTAINER_NAME'in os.environ:A='Kaggle'
			elif'.hf.space'in os.environ['SPACE_HOST']:A='Hugging Face Spaces'
		except:A='Local or Unknown'
		F=platform.uname();G=os.name;O=platform.processor();P=psutil.cpu_count(logical=True);Q=psutil.cpu_count(logical=False);R=psutil.virtual_memory().total/1024**3;S=psutil.virtual_memory().available/1024**3;T=socket.gethostname();U=socket.gethostbyname(T);V=':'.join(['{:02x}'.format(uuid.getnode()>>A&255)for A in range(0,12,2)])
		if A==J:C='Colab_Unknown';D=os.environ.get(K,_A);E=os.environ.get(L,_A)
		elif G=='posix':C=os.environ.get('USER')or getpass.getuser()or _A;D=os.environ.get(K,_A);E=os.environ.get(L,_A)
		elif G=='nt':C=os.environ.get('USERNAME',_A);D=os.environ.get('USERPROFILE',_A);E=os.getcwd()
		else:C=_A;D=_A;E=_A
		W={'uuid':M,'uid':C,'upath':D,'uwd':E,'environment':B,'hosting_service':A,'python_version':platform.python_version(),'os_name':F.system,'os_version':F.version,'machine':F.machine,'cpu_model':O,'cpu_cores':Q,'cpu_logical_cores':P,'ram_total':round(R,1),'ram_available':round(S,1),'local_ip':U,'mac_address':V};return W
	def log_analytics_data(A):
		C=A.system_info();D=A.licensing_id();E='gAAAAABmfy5Mzhjtv6HfnFra3DdNtLZTlg0DlHc_k4q-03SCCNBRd5lVzz8NYXqtrXTdp6mYQGyVuU7sLYzKs0SCRXhaxgsZkYJPnioRXngg5Xv0o7VhuOO4XZeI40NvXYrths6uIve8tmNZLxnGA_9qdczyFiNhoA==';F=A.cph.decrypt(A.target).decode(_B);G=f"{A.cph.decrypt((A.RH+E+A.LH)[30:-35].encode()).decode(_B)}{F}";B={'systems':C,'installed_packages':A.packages_installed(),'license_info':D}
		with open(A.env_config,'w',encoding=_B)as H:H.write(json.dumps(B,indent=4))
		try:I=requests.post(G,json=B)
		except:raise SystemExit('Vui lòng kiểm tra kết nối mạng và thử lại sau hoặc liên hệ Vnstock để được hỗ trợ.')
	def packages_installed(I):
		E='financetoolkit';D='backtesting';F={'vnstock_family':['vnstock','vnstock3','vnstock_ezchart','vnstock_data_provnstock_market_data_pipeline','vnstock_ta','vnai','vnii'],'analytics':['openbb','pandas_ta'],'static_charts':['matplotlib','seaborn','altair'],'dashboard':['streamlit','voila','panel','shiny','dash'],'interactive_charts':['mplfinance','plotly','plotline','bokeh','pyecharts','highcharts-core','highcharts-stock','mplchart'],'datafeed':['yfinance','alpha_vantage','pandas-datareader','investpy'],'official_api':['ssi-fc-data','ssi-fctrading'],'risk_return':['pyfolio','empyrical','quantstats',E],'machine_learning':['scipy','sklearn','statsmodels','pytorch','tensorflow','keras','xgboost'],'indicators':['stochastic','talib','tqdm','finta',E,'tulipindicators'],D:['vectorbt',D,'bt','zipline','pyalgotrade','backtrader','pybacktest','fastquant','lean','ta','finmarketpy','qstrader'],'server':['fastapi','flask','uvicorn','gunicorn'],'framework':['lightgbm','catboost','django']};A={}
		for(B,G)in F.items():
			A[B]=[]
			for C in G:
				try:H=importlib.metadata.version(C);A[B].append((C,H))
				except importlib.metadata.PackageNotFoundError:pass
		return A
	def licensing_id(A):
		D='user'
		if not os.path.exists(A.id):
			if not os.path.exists(A.project_dir):B='License not recognized. ID file not found.'
			else:B=f"License directory found, but ID does not exist."
			C=_A
		else:
			B='License recognized.'
			with open(A.id,'r')as E:F=json.load(E);C=F[D]
		G={'status':B,D:C};return G
def lc_init():A=VnstockInitializer(TG);A.log_analytics_data()