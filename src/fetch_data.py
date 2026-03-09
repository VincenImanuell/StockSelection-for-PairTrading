import numpy as np
import pandas as pd
import yfinance as yf

# Categorized ticker symbol by sector in Indonesia stock market
sektor = {
    "industri": [
        "AMIN","APII","ARNA","ASGR","ASII","BHIT","BNBR","CTTH","DYAN",
        "HEXA","IBFN","ICON","IKAI","IKBI","IMPC","INDX","INTA","JECC","JTPE",
        "KBLI","KBLM","KIAS","KOBX","KOIN","KONI","LION","MDRN","MFMI","MLIA",
        "SCCO","TIRA","TOTO","TRIL","UNTR","VOKS","ZBRA"
    ],

    "energi": [
        "ABMM","ADRO","AIMS","AKRA","APEX","ARII","ARTI","BBRM","BIPI","BSSR",
        "BULL","BUMI","BYAN","CANI","CNKO","DEWA","DOID","DSSA","ELSA","ENRG",
        "GEMS","GTBO","HITS","HRUM","IATA","INDY","ITMA","ITMG","KKGI","KOPI",
        "LEAD","MBAP","MBSS","MEDC","MTFN","MYOH","PGAS","PKPK","PTBA","PTIS",
        "PTRO","RAJA","RIGS","RUIS","SMMT","SMRU","SOCI","SUGI","TOBA","TPMA",
        "TRAM","WINS"
    ],

    "barang_baku": [
        "ADMG","AKPI","ALDO","ALKA","ALMI","ANTM","APLI","BAJA","BMSR","BRMS",
        "BRNA","BRPT","BTON","CITA","CLPI","CTBN","DKFT","DPNS","EKAD","ESSA",
        "ETWA","FASW","FPNI","GDST","IGAR","INAI","INCI","INCO","INKP","INRU",
        "INTD","INTP","IPOL","ISSP","KBRI","KDSI","KRAS","LMSH","LTLS","MDKA",
        "NIKL","OKAS","PICO","PSAB","SIMA","SMBR","SMCB","SMGR","SPMA","SQMI",
        "SRSN","SULI","TALF","TBMS","TINS","TIRT","TKIM","TPIA","TRST","UNIC",
        "WTON","YPAS", "AMFG"
    ],

    "infrastruktur": [
        "ACST","ADHI","BALI","BTEL","BUKK","CASS","CENT","CMNP","DGIK","EXCL",
        "GOLD","HADE","IBST","ISAT","JKON","JSMR","KARW","KBLV","LINK","META",
        "NRCA","PTPP","SSIA","SUPR","TBIG","TLKM","TOTL","TOWR","WIKA","WSKT",
        "IDPR"
    ],

    "transport_logistik": [
        "AKSI","ASSA","BIRD","BLTA","CMPP","GIAA","IMJS","LRNA","MIRA","MITI",
        "NELY","SAFE","SDMU","SMDR","TMAS","WEHA","TAXI"
    ],

    "keuangan": [
        "ABDA","ADMF","AGRO","AGRS","AHAP","AMAG","APIC","ASBI","ASDM","ASJT",
        "ASMI","ASRM","BABP","BACA","BBCA","BBHI","BBKP","BBLD","BBMD","BBNI",
        "BBRI","BBTN","BBYB","BCAP","BCIC","BDMN","BEKS","BFIN","BINA","BJBR",
        "BJTM","BKSW","BMAS","BMRI","BNBA","BNGA","BNII","BNLI","BPFI","BPII",
        "BSIM","BSWD","BTPN","BVIC","CFIN","DEFI","DNAR","DNET","GSMF","HDFA",
        "INPC","LPGI","LPPS","MAYA","MCOR","MEGA","MREI","NISP","NOBU","OCAP",
        "PADI","PALM","PANS","PEGE","PLAS","PNBN","PNBS","PNIN","PNLF","POOL",
        "RELI","SDRA","SMMA","SRTG","STAR","TIFA","TRIM","TRUS","VICO","VINS",
        "VRNA","WOMF","YULE"
    ],

    "properti": [
        "APLN","ASRI","BAPA","BCIP","BEST","BIKA","BIPP","BKDP","BKSL","BSDE",
        "COWL","CTRA","DART","DILD","DMAS","DUTI","ELTY","EMDE","FMII","GAMA",
        "GMTD","GPRA","INPP","JRPT","KIJA","LCGP","LPCK","LPKR","LPLI","MDLN",
        "MKPI","MMLP","MTLA","MTSM","NIRO","OMRE","PLIN","PPRO","PUDP","PWON",
        "RBMS","RDTX","RIMO","RODA","SMDM","SMRA","TARA"
    ],

    "teknologi": [
        "ATIC","EMTK","KREN","LMAS","MLPT","MTDL","PTSN","SKYB"
    ],

    "consumer_cyclical": [
        "ABBA","ACES","AKKU","ARGO","ARTA","AUTO","BATA","BAYU","BIMA","BLTZ",
        "BMTR","BOLT","BRAM","BUVA","CINT","CNTX","CSAP","ECII","ERAA","ERTX",
        "ESTI","FAST","FORU","GDYR","GEMA","GJTL","GLOB","GWSA","HOME","HOTL",
        "IIKP","IMAS","INDR","INDS","JIHD","JSPT","KICI","KPIG","LMPI","LPIN",
        "LPPF","MAPI","MDIA","MGNA","MICE","MNCN","MPMX","MSKY","MYTX","PANR",
        "PBRX","PDES","PGLI","PJAA","PNSE","POLY","PSKT","PTSP","RALS","RICY",
        "SCMA","SHID","SMSM","SONA","SRIL","SSTM","TELE","TFCO","TMPO","TRIO",
        "TRIS","UNIT","VIVA","MKNT"
    ],

    "consumer_non_cyclical": [
        "AALI","ADES","AISA","ALTO","AMRT","ANJT","BISI","BTEK","BUDI","BWPT",
        "CEKA","CPIN","CPRO","DLTA","DSFI","DSNG","EPMT","FISH","GGRM","GOLL",
        "GZCO","HERO","HMSP","ICBP","INDF","JAWA","JPFA","LAPD","LSIP","MAGP",
        "MAIN","MBTO","MIDI","MLBI","MLPL","MPPA","MRAT","MYOR","PSDN","RANC",
        "ROTI","SDPC","SGRO","SIMP","SIPD","SKBM","SKLT","SMAR","SSMS","STTP",
        "TBLA","TCID","TGKA","ULTJ","UNSP","UNVR","WAPO","WICO","WIIM","DAYA",
        "DPUM","KINO"
    ],

    "kesehatan": [
        "DVLA","INAF","KAEF","KLBF","MERK","MIKA","PYFA","SAME","SCPI","SIDO",
        "SILO","SRAJ","TSPC"
    ]
}

# Gabungkan semua kode dari dictionary sektor
kode_sektor = []
for daftar in sektor.values():
    kode_sektor.extend(daftar)

valid_tickers = list(set(kode_sektor))


def download(tickers):
    start_date = "2016-01-01"
    end_date   = "2019-12-31"   
    prices = pd.DataFrame()
    valid_tickers = []  
    for kode in tickers:
        try:
            df = yf.download(kode + ".JK", start=start_date, end=end_date, multi_level_index=False) 
            # cek apakah data kosong
            if df.empty:
                print(f"Data kosong {kode}")
                continue    
            # cek apakah close semuanya NaN
            if df["Close"].isna().all():
                print(f"Close harga kosong {kode}")
                continue    
            # cek minimal 200 data
            if len(df) < 200:
                print(f"Terlalu sedikit data {kode}")
                continue    
            prices[kode] = df["Close"]
            valid_tickers.append(kode)  
        except Exception as e:
            print(f"Error pada {kode}: {e}")    
    print("\n=== SAHAM YANG BERHASIL DIAMBIL DATANYA ===")
    print(valid_tickers)    
    print("\n=== PREVIEW DATAFRAME ===")
    print(prices.head())    
    all_df = dict()

    for nama_sektor, tickers in sektor.items():
        print(f"=== Sektor: {nama_sektor} ===")

        tickers_aktif = [t for t in tickers if t in kode_sektor]

        if len(tickers_aktif) == 0:
            print("⚠ Tidak ada saham aktif di sektor ini.\n")
            continue

        df = download(tickers_aktif)
        all_df[nama_sektor] = df

        print(f"Selesai sektor {nama_sektor}, shape: {df.shape}\n")
        
        return all_df
    
def preproccess(all_df):
    aligned_df = {}
    for sektor, df_sektor in all_df.items():
        # Buang baris yang punya missing value
        df_aligned = df_sektor.dropna()

        # Simpan kembali
        aligned_df[sektor] = df_aligned

        print(sektor, df_sektor.shape, "→", df_aligned.shape)
    cleaned_df = {}

    for sektor, df_sektor in all_df.items():

        # hitung persentase missing per saham
        missing_ratio = df_sektor.isna().mean()

        # hanya ambil saham dengan missing < 5%
        saham_valid = missing_ratio[missing_ratio < 0.05].index

        df_filtered = df_sektor[saham_valid]

        cleaned_df[sektor] = df_filtered

        print(sektor, "→", df_filtered.shape)
        
    for sektor in cleaned_df:
        cleaned_df[sektor] = cleaned_df[sektor].dropna()
        
    for sektor, df_sektor in cleaned_df.items():
        std = df_sektor.std()

        saham_aktif = std[std > 0].index
        cleaned_df[sektor] = df_sektor[saham_aktif]
        
    for sektor, df_sektor in cleaned_df.items():
        print(sektor, df_sektor.shape[1])
        
    return cleaned_df
    