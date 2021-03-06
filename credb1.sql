drop table CorpOutline purge;
drop table Affiliate purge;
drop table ConsSubsComp purge;

create table CorpOutline
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
corpNm VARCHAR2(1000),
corpEnsnNm VARCHAR2(1000),
enpPbanCmpyNm VARCHAR2(1000),
enpRprFnm VARCHAR2(150),
corpRegMrktDcd VARCHAR2(1),
corpRegMrktDcdNm VARCHAR2(100),
corpDcd VARCHAR2(2),
corpDcdNm VARCHAR2(100),
bzno VARCHAR2(10),
enpOzpno VARCHAR2(6),
enpBsadr VARCHAR2(500),
enpDtadr VARCHAR2(500),
enpHmpgUrl VARCHAR2(300),
enpTlno VARCHAR2(100),
enpFxno VARCHAR2(100),
sicNm VARCHAR2(1000),
enpEstbDt VARCHAR2(8),
enpStacMm VARCHAR2(2),
enpXchgLstgDt VARCHAR2(8),
enpXchgLstgAbolDt VARCHAR2(8),
enpKosdaqLstgDt VARCHAR2(8),
enpKosdaqLstgAbolDt VARCHAR2(8),
enpKrxLstgDt VARCHAR2(8),
enpKrxLstgAbolDt VARCHAR2(8),
smenpYn VARCHAR2(1),
enpMntrBnkNm VARCHAR2(100),
enpEmpeCnt VARCHAR2(9),
empeAvgCnwkTermCtt VARCHAR2(100),
enpPn1AvgSlryAmt NUMBER(22,3),
actnAudpnNm VARCHAR2(1000),
audtRptOpnnCtt VARCHAR2(100),
enpMainBizNm VARCHAR2(1000),
fssCorpUnqNo VARCHAR2(8),
fssCorpChgDtm VARCHAR2(20)
);

create table Affiliate
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
afilCmpyNm VARCHAR2(1000),
afilCmpyCrno VARCHAR2(13),
lstgYn VARCHAR2(1)
);

create table ConsSubsComp
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
sbrdEnpNm VARCHAR2(150),
sbrdEnpEstbDt VARCHAR2(8),
sbrdEnpAdr VARCHAR2(500),
sbrdEnpMainBizCtt VARCHAR2(500),
dntRltBsisCtt VARCHAR2(500),
mainSbrdEnpYnCtt VARCHAR2(500)
sbrdEnpLtstEbzyrTastAmt NUMBER(18),
);


COMMENT ON TABLE CorpOutline is '기업개요조회';
COMMENT ON TABLE Affiliate is '계열회사조회';
COMMENT ON TABLE ConsSubsComp is '연결대상종속기업조회';

COMMENT ON COLUMN CorpOutline.basDt is '기준일자';
COMMENT ON COLUMN CorpOutline.crno is '법인등록번호';
COMMENT ON COLUMN CorpOutline.corpNm is '법인명';
COMMENT ON COLUMN CorpOutline.corpEnsnNm is '법인영문명';
COMMENT ON COLUMN CorpOutline.enpPbanCmpyNm is '기업공시회사명';
COMMENT ON COLUMN CorpOutline.enpRprFnm is '기업대표자성명';
COMMENT ON COLUMN CorpOutline.corpRegMrktDcd is '법인등록시장구분코드';
COMMENT ON COLUMN CorpOutline.corpRegMrktDcdNm is '법인등록시장구분코드명';
COMMENT ON COLUMN CorpOutline.corpDcd is '법인구분코드';
COMMENT ON COLUMN CorpOutline.corpDcdNm is '법인구분코드명';
COMMENT ON COLUMN CorpOutline.bzno is '사업자등록번호';
COMMENT ON COLUMN CorpOutline.enpOzpno is '기업구우편번호';
COMMENT ON COLUMN CorpOutline.enpBsadr is '기업기본주소';
COMMENT ON COLUMN CorpOutline.enpDtadr is '기업상세주소';
COMMENT ON COLUMN CorpOutline.enpHmpgUrl is '기업홈페이지URL';
COMMENT ON COLUMN CorpOutline.enpTlno is '기업전화번호';
COMMENT ON COLUMN CorpOutline.enpFxno is '기업팩스번호';
COMMENT ON COLUMN CorpOutline.sicNm is '표준산업분류명';
COMMENT ON COLUMN CorpOutline.enpEstbDt is '기업설립일자';
COMMENT ON COLUMN CorpOutline.enpStacMm is '기업결산월';
COMMENT ON COLUMN CorpOutline.enpXchgLstgDt is '기업거래소상장일자';
COMMENT ON COLUMN CorpOutline.enpXchgLstgAbolDt is '기업거래소상장폐지일자';
COMMENT ON COLUMN CorpOutline.enpKosdaqLstgDt is '기업코스닥상장일자';
COMMENT ON COLUMN CorpOutline.enpKosdaqLstgAbolDt is '기업코스닥상장폐지일자';
COMMENT ON COLUMN CorpOutline.enpKrxLstgDt is '기업KONEX상장일자';
COMMENT ON COLUMN CorpOutline.enpKrxLstgAbolDt is '기업KONEX상장폐지일자';
COMMENT ON COLUMN CorpOutline.smenpYn is '중소기업여부';
COMMENT ON COLUMN CorpOutline.enpMntrBnkNm is '기업주거래은행명';
COMMENT ON COLUMN CorpOutline.enpEmpeCnt is '기업종업원수';
COMMENT ON COLUMN CorpOutline.empeAvgCnwkTermCtt is '종업원평균근속기간내용';
COMMENT ON COLUMN CorpOutline.enpPn1AvgSlryAmt is '기업1인평균급여금액';
COMMENT ON COLUMN CorpOutline.actnAudpnNm is '회계감사인명';
COMMENT ON COLUMN CorpOutline.audtRptOpnnCtt is '감사보고서의견내용';
COMMENT ON COLUMN CorpOutline.enpMainBizNm is '기업주요사업명';
COMMENT ON COLUMN CorpOutline.fssCorpUnqNo is '금융감독원법인고유번호';
COMMENT ON COLUMN CorpOutline.fssCorpChgDtm is '금융감독원법인변경일시';

COMMENT ON COLUMN Affiliate.basDt is '기준일자';
COMMENT ON COLUMN Affiliate.crno is '법인등록번호';
COMMENT ON COLUMN Affiliate.afilCmpyNm is '계열회사명';
COMMENT ON COLUMN Affiliate.afilCmpyCrno is '계열회사법인등록번호';
COMMENT ON COLUMN Affiliate.lstgYn is '상장여부';

COMMENT ON COLUMN ConsSubsComp.basDt is '기준일자';
COMMENT ON COLUMN ConsSubsComp.crno is '법인등록번호';
COMMENT ON COLUMN ConsSubsComp.sbrdEnpNm is '종속기업명';
COMMENT ON COLUMN ConsSubsComp.sbrdEnpEstbDt is '종속기업설립일자';
COMMENT ON COLUMN ConsSubsComp.sbrdEnpAdr is '종속기업주소';
COMMENT ON COLUMN ConsSubsComp.sbrdEnpMainBizCtt is '종속기업주요사업내용';
COMMENT ON COLUMN ConsSubsComp.sbrdEnpLtstEbzyrTastAmt is '종속기업최근사업연도말총자산금액';
COMMENT ON COLUMN ConsSubsComp.dntRltBsisCtt is '지배관계근거내용';
COMMENT ON COLUMN ConsSubsComp.mainSbrdEnpYnCtt is '주요종속기업여부내용';

create table SummFinaStat
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
bizYear VARCHAR2(4),
fnclDcd VARCHAR2(35),
fnclDcdNm VARCHAR2(100),
enpSaleAmt NUMBER(22,3),
enpBzopPft NUMBER(22,3),
iclsPalClcAmt NUMBER(22,3),
enpCrtmNpf NUMBER(22,3),
enpTastAmt NUMBER(22,3),
enpTdbtAmt NUMBER(22,3),
enpTcptAmt NUMBER(22,3),
enpCptlAmt NUMBER(22,3),
fnclDebtRto NUMBER(26,10)
);

create table bs
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
bizYear VARCHAR2(4),
fnclDcd VARCHAR2(35),
fnclDcdNm VARCHAR2(100),
acitId VARCHAR2(200),
acitNm VARCHAR2(1000),
thqrAcitAmt NUMBER(22,3),
crtmAcitAmt NUMBER(22,3),
lsqtAcitAmt NUMBER(22,3),
pvtrAcitAmt NUMBER(22,3),
bpvtrAcitAmt NUMBER(22,3)
);

create table IncoStat
(
basDt VARCHAR2(8),
crno VARCHAR2(13),
bizYear VARCHAR2(4),
fnclDcd VARCHAR2(35),
fnclDcdNm VARCHAR2(100),
acitId VARCHAR2(200),
acitNm VARCHAR2(1000),
thqrAcitAmt NUMBER(22,3),
crtmAcitAmt NUMBER(22,3),
lsqtAcitAmt NUMBER(22,3),
pvtrAcitAmt NUMBER(22,3),
bpvtrAcitAmt NUMBER(22,3)
);

COMMENT ON TABLE SummFinaStat is '요약재무제표조회';
COMMENT ON TABLE Bs is '재무상태표조회';
COMMENT ON TABLE IncoStat is '손익계산서조회';

COMMENT ON COLUMN SummFinaStat.basDt is '기준일자';
COMMENT ON COLUMN SummFinaStat.crno is '법인등록번호';
COMMENT ON COLUMN SummFinaStat.bizYear is '사업연도';
COMMENT ON COLUMN SummFinaStat.fnclDcd is '재무제표구분코드';
COMMENT ON COLUMN SummFinaStat.fnclDcdNm is '재무제표구분코드명';
COMMENT ON COLUMN SummFinaStat.enpSaleAmt is '기업매출금액';
COMMENT ON COLUMN SummFinaStat.enpBzopPft is '기업영업이익';
COMMENT ON COLUMN SummFinaStat.iclsPalClcAmt is '포괄손익계산금액';
COMMENT ON COLUMN SummFinaStat.enpCrtmNpf is '기업당기순이익';
COMMENT ON COLUMN SummFinaStat.enpTastAmt is '기업총자산금액';
COMMENT ON COLUMN SummFinaStat.enpTdbtAmt is '기업총부채금액';
COMMENT ON COLUMN SummFinaStat.enpTcptAmt is '기업총자본금액';
COMMENT ON COLUMN SummFinaStat.enpCptlAmt is '기업자본금액';
COMMENT ON COLUMN SummFinaStat.fnclDebtRto is '재무제표부채비율';

COMMENT ON COLUMN Bs.basDt is '기준일자';
COMMENT ON COLUMN Bs.crno is '법인등록번호';
COMMENT ON COLUMN Bs.bizYear is '사업연도';
COMMENT ON COLUMN Bs.fnclDcd is '재무제표구분코드';
COMMENT ON COLUMN Bs.fnclDcdNm is '재무제표구분코드명';
COMMENT ON COLUMN Bs.acitId is '계정과목ID';
COMMENT ON COLUMN Bs.acitNm is '계정과목명';
COMMENT ON COLUMN Bs.thqrAcitAmt is '당분기계정과목금액';
COMMENT ON COLUMN Bs.crtmAcitAmt is '당기계정과목금액';
COMMENT ON COLUMN Bs.lsqtAcitAmt is '전분기계정과목금액';
COMMENT ON COLUMN Bs.pvtrAcitAmt is '전기계정과목금액';
COMMENT ON COLUMN Bs.bpvtrAcitAmt is '전전기계정과목금액';

COMMENT ON COLUMN IncoStat.basDt is '기준일자';
COMMENT ON COLUMN IncoStat.crno is '법인등록번호';
COMMENT ON COLUMN IncoStat.bizYear is '사업연도';
COMMENT ON COLUMN IncoStat.fnclDcd is '재무제표구분코드';
COMMENT ON COLUMN IncoStat.fnclDcdNm is '재무제표구분코드명';
COMMENT ON COLUMN IncoStat.acitId is '계정과목ID';
COMMENT ON COLUMN IncoStat.acitNm is '계정과목명';
COMMENT ON COLUMN IncoStat.thqrAcitAmt is '당분기계정과목금액';
COMMENT ON COLUMN IncoStat.crtmAcitAmt is '당기계정과목금액';
COMMENT ON COLUMN IncoStat.lsqtAcitAmt is '전분기계정과목금액';
COMMENT ON COLUMN IncoStat.pvtrAcitAmt is '전기계정과목금액';
COMMENT ON COLUMN IncoStat.bpvtrAcitAmt is '전전기계정과목금액';



CREATE TABLE TOT_CNT_BAS_DT
(
    TBL_NM VARCHAR2(100),
    BAS_DT VARCHAR2(8),
    TOT_CNT NUMBER(20)
)
;
CREATE TABLE TOT_CNT_BIZ_YEAR
(
    TBL_NM VARCHAR2(100),
    BIZ_YEAR VARCHAR2(8),
    TOT_CNT NUMBER(20)
)
;   