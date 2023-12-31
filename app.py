import random
from flask import Flask, render_template, request

app = Flask(__name__)

# 객관식 퀴즈 문제와 답안
multiple_choice_questions = [
    {
        'question': '다음 중 불법탈법차명거래에 해당하지 않는 것은?',
        'choices': ['불법재산의 은닉', '자금세탁행위(조세포탈 등)', '공중협박자금조달행위', ' 강제집행의 면탈','대가 없는 증여거래'],
        'answer': '대가 없는 증여거래'
    },
    {
        'question':'어음이나 수표를 가진 사람이 기한이 되어도 어음이나 수표에 해당하는 금액을 현금으로 지급받지 못하는 것에 대한 올바른 용어는 무엇인가?',
        'choices':['부도','상계','유가증권','타행환','전결권'],
        'answer':'부도'
    },
    {
        'question':'채무자와 채권자가 서로 동종의 채권.채무를 갖는 경우에 채무자의 일방적 의사표시에 의하여 그 채권, 채무를 대등액에서 소멸시키는 것을 말하는 것은?',
        'choices':['상계','부도','기명','약관','대체'],
        'answer':'상계'
    },
    {
        'question':'재산적 가치를 가지는 사권을 표시하는 증권으로 해당증권의 점유를 통해 청구권 및 소유권을 행사할수 있는 것은?',
        'choices':['유가증권','채무증권','지분증권','수익증권','투자계약증권'],
        'answer':'유가증권'
    },
    {
        'question':'서로 다른 은행간에 이루어지는 자금의 이동을 뜻하는 용어는?',
        'choices':['타행환','증여거래','송금환','추심환','예치환'],
        'answer':'타행환'
    },
    {
        'question':'결재를 하는 직책의 관리자가 가지고 있는 결재에 대한 권리에 대한 적절한 용어는?',
        'choices':['전결권','의사결정권','송금권','추심권','담보권'],
        'answer':'전결권'
    },
    {
        'question':'금융기관이 공동으로 사용할 목적으로 금융기관공동코드위원회가 제정한 코드로서 총 6자리로 구성되는데 은행코드 3자리와 지점코드 3자리로 구성되며 마지막 한자리는 자동생성되는 검증번호(CheckDigit)이며 은행코드(000)+지점코드(000)+(0)에 대한 올바른 용어는?',
        'choices':['지로코드','SWIFT코드','소스코드','퍼블릭코드','오픈코드'],
        'answer':'지로코드'
    },
    {
        'question':'직무상 쓰는 도장으로 문서의 확인을 위해 찍는 것으며 직책이 앞에 합성되어 주로 사용되는 것은?',
        'choices':['직인','수관','부도','상계','이관'],
        'answer':'직인'
    },
    {
        'question':'은행 업무상 책임 및 권한을 가진 자를 뜻하는 용어는?',
        'choices':['책임자','결정권자','운영자','관리자','대체자'],
        'answer':'책임자'
    },
    {
        'question':'수표 표면 상단에 두 줄의 평행선을 표시한 수표로 은행 또는 지급인의 거래처에 대해서만 지급할 수 있는 수표에 대한 용어는?',
        'choices':['횡선수표','평행선수표','종단선수표','거래수표','무기명수표'],
        'answer':'횡선수표'
    },
    {
        'question':'통장이나 IC (현금)카드 뒷면에 붙어있는 폭이 얇은 검은색 자기대를 말하는 용어는?',
        'choices':['M/S','M/F','S/M','M/O','I/O'],
        'answer':'M/S'
    },
    {
        'question':'계좌에 대한 실적을 관리하는 지점으로 일반적으로는 계좌를 최초개설한 지점이며 거래후 변경도 가능한 지점을 뜨ㅡㅅ하는 것은?',
        'choices':['계좌관리점','최초개설점','계좌등록점','주거래지점','계좌개설점'],
        'answer':'계좌관리점'
    },
    {
        'question':'예금개설 후 영업점외 같은 은행의 타영업점을 모두 "이것"점이라고 하며,개설점 이외의 타영업점에서의 거래를 "이것"거래라고 한다. 이것은?',
        'choices':['NET','MOU','NFT','NMF','NPV'],
        'answer':'NET'
    },
    {
        'question':'객관적인 금융거래목적 증빙자료를 제출하지 못하는 고객을 대상으로 일일 출금이체한도를 100만원으로 제한하는 계좌는?',
        'choices':['한도제한계좌','거래제한계좌','송금제한계좌','출금제한계좌','이체제한계좌'],
        'answer':'한도제한계좌'
    },
    {
        'question':'개설요청일 포함 20영업일 이내 당행 또는 다른 금융회사에서 1개 이상의 입출금이 자유로운 예금을 개설하고 당행에서 2번째 이후로 개설하고자 하는 입출금이 자유로운 계좌는?',
        'choices':['단기간다수계좌','이상거래계좌','다수거래계좌','장기간다수계좌','중기간다수계좌'],
        'answer':'단기간다수계좌'
    },
    {
        'question':'범죄행위로부터 얻은 불법자금의 출처를 숨기고 합법적인 자산인 것처럼 위장하는 행위는?',
        'choices':['자금세탁행위','자금탈세행위','자금위탁행위','자금절도행위','자금전용행위'],
        'answer':'자금세탁행위'
    },
    {
        'question':'소득을 지급하는 자(원천징수의무자)가, 소득금액 또는 수입금액에 대하여 정부를 대신하여 납세의무자의 세액을 징수하여 정부에 납부하는 제도는?',
        'choices':['원천징수','단기징수','대납징수','보통징수','특별징수'],
        'answer':'원천징수'
    },
    {
        'question':'일정한 기간을 정하여 일정한 금액을 지급할 것을 약정하고 매월 약정한 날짜에 월 저축금을 입금하는 예금은?',
        'choices':['정기적금','자유적금','보통예금','적립적금','고금리적금'],
        'answer':'정기적금'
    },
    {
        'question':'약정기간 동안 가입자가 여유자금이 있을 때 수시로 적립할 수 있는 상품은?',
        'choices':['자유적금','정기적금','보통예금','적립적금','고금리적금'],
        'answer':'자유적금'
    },
    {
        'question':'계좌 관리점을 변경하는 작업처리. "이것"은 계좌관리점을 우리지점에서 다른 지점으로 보내주는 것을 말하며, "이것"은 관리점을 다른 지점에서 우리 지점으로 옮겨오는 것을 말한다. 올바르게 짝지어 진것은?',
        'choices':['이관,수관','이관,회관','전관,회관','송관,수관','전관,수관'],
        'answer':'이관,수관'
    },
    {
        'question':'가계여신 신청인 및 보증인에 대한 신용평점을 통계적 모형에 의해 산출하고, 여신의 신청 및 심사 등을 자동화된 프로세스에 의해 수행함으로써 일관성을 제고하도록 설계된 우리은행의 시스템은?',
        'choices':['가계여신 신용평점 시스템','가계여신 자동화 평점 시스템','가계여신 통계 시스템','가계여신 정보평가 시스템','가계여신 신용평가 시스템'],
        'answer':'가계여신 신용평점 시스템'
    },
    {
        'question':'신용평점 결과에 따라 1~10등급으로 구분하는 은행 자체 신용평모형에 의한 당행 내부 등급은? (당행 내부 정보 포함으로 상위등급 변별력 높음)',
        'choices':['CSS등급','BRR등급','CRM등급','IRP등급','LPV등급'],
        'answer':'CSS등급'
    },
    {
        'question':'업여신 거래상대방의 채무불이행 가능성을 판단하여 산출하는 신용등급은? (AAA~D 영문표시 방식의 14등급 체계로 구성)',
        'choices':['차주신용등급','신용평가등급','채무평가등급','불이행가능성등급','위험평가등급'],
        'answer':'차주신용등급'
    },
    {
        'question':' 우리은행 여신업무에서 "이것"은 차주, 보증인, 담보제공자 등을 말하며, "이것"이 될 수 있는 자는 자연인, 법인, 조합 및 단체로 한다. 이것은?',
        'choices':['채무관계인','거래관계인','보증관계인','담보관계인','차주관계인'],
        'answer':'채무관계인'
    },
    {
        'question':'은행이 직접 자금을 부담하는 금전에 의한 신용공여에 대해 올바른 용어는?',
        'choices':['대출','여신','수신','담보','보증'],
        'answer':'대출'
    },
    {
        'question':'은행이 직접 자금을 부담하는 대출뿐 아니라 직접적인 자금부담이 없는 신용공여를 포함하는 개념은?',
        'choices':['여신','수신','대출','담보','보증'],
        'answer':'여신'
    },
    {
        'question':'여신금액 범위내에서 일괄(또는 분할)하여 대출을 취급하되, 상환한 금액을 재취급 할 수 없는 거래는?',
        'choices':['건별거래','한도거래','당좌거래','대출거래','여신거래'],
        'answer':'건별거래'
    },
    {
        'question':'새로운 약정에 의해 여신을 처음으로 취급하는 것으로 기 취급여신의 대환을 포함하는 것은?',
        'choices':['신규','차환','기신','증대','연장'],
        'answer':'신규'
    },
    {
        'question':'기 취급여신의 약정기간 범위 내에서 여신잔액이나 약정한도를 더하여 취급하는 것을 말하는 것은?',
        'choices':['증대','한도','담보','신규','연장'],
        'answer':'증대'
    },
    {
        'question':'가계여신의 만기가 1개월(기업여신은 3개월) 이내로 도래하거나 기일이 경과한 여신의 만기일을 연장하는 것은?',
        'choices':['기간연장','한도연장','계약연장','상환연장','대출연장'],
        'answer':'기간연장'
    },
    {
        'question':'가계여신의 만기가 1개월(기업여신은 3개월) 이내로 도래하거나 기일이 경과한 기 취급 여신을 동일차주, 동일과목(상품) 및 동일금액 이내에서 재취급하는 것',
        'choices':['재약정','동일약정','확정','신규','증대'],
        'answer':'재약정'
    },
    {
        'question':'기 취급한 여신의 차주, 과목(상품), 금액, 기간을 제외한 거래 조건을 변경하는 것을 말하는 것은?',
        'choices':['조건변경','재약정','조건확정','조건회부','조건계약'],
        'answer':'조건변경'
    },
    {
        'question':'금융거래 등 상거래에 있어서 거래상대방에 대한 신용도 등의 판단을 위하여 필요로 하는 식별정보, 신용거래정보, 금융문란정보 등 종합신용정보집중기관에서 관리하는 정보는?',
        'choices':['신용정보','개인정보','계약정보','심층정보','보안정보'],
        'answer':'신용정보'
    },
    {
        'question':'대출원금, 이자등을 3개월 이상 연체한 거래처, 5만원 이상의 신용카드 대금을 3개월 이상 연체한 거래처, "이것" 관련인 등에 대해 이것은?',
        'choices':['유의거래처','위험거래처','개인거래처','보안거래처','주의거래처'],
        'answer':'유의거래처'
    },
    {
        'question':'채무불이행 시 채무변제를 확보하는 수단으로 채권자에게 제공하는 것으로 저당권/질권/ 지상권 등의 물적 "이것"과 보증채무 / 연대채무 등의 인적 "이것"이 있다. 이것은?',
        'choices':['담보','보증','채권','요인','권리'],
        'answer':'담보'
    },
    {
        'question':'채무자가 채무를 이행하지 아니할 경우에, 채무자를 대신하여 채무를 이행할 것을 부담하는 것은?',
        'choices':['보증','담보','채권','대출','권리'],
        'answer':'보증'
    },
    {
        'question':'보증인이 주채무자와 연대하여 채무를 부담하는 보증채무를 의미하는 것은?',
        'choices':['연대보증','공동보증','유연보증','공통보증','연계보증'],
        'answer':'연대보증'
    },
    {
        'question':'채무자가 약정된 기한까지 누릴수 있는 이익이 상실되는 것을 말한다. 기한의 이익은 포기할 수 있으나, 이자가 붙은 차금을 기한전에 변제할 경우는 대주의 손해를 배상하지 않으면 안되는 것을 의미하는 것은?',
        'choices':['기한의 이익 상실','기한의 이자 상실','기한의 권리 상실','기한의 원금 상실','기한의 계약 상실'],
        'answer':'기한의 이익 상실'
    },
    {
        'question':'연체대출채권에 대하여 부과하는 이자율로 최고지연배상금율은 가계 12%, 기업 15%를 초과할 수 없는 것은?',
        'choices':['지연배상금율','지연인상률','지연확대율','지연연체금율','지연이자금율'],
        'answer':'지연배상금율'
    },
    {
        'question':'동일차주에 대한 당행 본지점 여신을 포함하여 직계별로 전결가능한 최고 여신한도를 말하며, 동일인 여신한도와 별도여신한도로 구분하는 것은?',
        'choices':['총여신한도','최고여신한도','전체여신한도','종합여신한도','전결여신한도'],
        'answer':'총여신한도'
    },
    {
        'question':'총여신한도에서 별도여신한도를 차감한 여신 한도',
        'choices':['동일인 여신한도','독립여신한도','종속여신한도','순여신한도','적정 여신한도'],
        'answer':'동일인 여신한도'
    },
    {
        'question':'"이것" 직무전결기준표에 명시된 여신과목 또는 담보 등에 대하여 동일인 여신한도에 추가하여 취급할 수 있는 직계별 여신한도로서 이것은?',
        'choices':['별도여신한도','독립여신한도','종속여신한도','추가여신한도','적정 여신한도'],
        'answer':'별도여신한도'
    },
    {
        'question':'일정한 사항에 대한 의사결정 및 집행과정에 있어 최종의 결재를 하는 권한을 가진 직계를 말하며, "이것" 행사에 따른 처리 결과에 대하여 책임을 지는 직책은?',
        'choices':['전결권자','의사결정권자','최종관리자','책임관리자','선임결제권자'],
        'answer':'전결권자'
    }
    # 나머지 문제들도 유사한 형태로 추가해주세요
    # {'question': '다음 중 가장 큰 수를 찾는 함수는?', 'choices': [...], 'answer': 'max()'}
    # ...
]

# 주관식 퀴즈 문제와 답안
open_questions = [
    {
        'question': '범죄자들이 경찰추적을 피하기 위한 목적으로 불법자금을 수수하거나 세탁하는데 사용하는 타인명의 통장은?',
        'answer': '대포통장'
    },
    {
        'question':'계약의 당사자가 다수의 상대방과 계약체결을 위하여 미리 작성한 계약은?',
        'answer':'약관'
    },
    {
        'question':'실명을 확인할 수 있는 증서, 실명확인증표는 주민등록증이 원칙이며 그 외의 실명확인증표(운전면허증,여권 등)는 예외적으로 사용 가능함을 뜻하는 것은?',
        'answer':'실명확인증표'
    },
    {
        'question':'당사자의 동의 없는 개인정보 수집 및 활용하거나 제3자에게 제공하는 것을 금지하는 등 개인정보보호를 강화한 내용을 담아 제정한 법률은?',
        'answer':'개인정보보호법'
    },
    {
        'question':'전기통신을 이용하여 불특정 다수인을 기망, 공갈함으로써 재산상의 이익을 취하거나 제3자에게 재산상의 이익을 취하게 하는 행위로, 주로 자금을 송금/이체하도록 하는 행위를 뜻하는 것은?',
        'answer':'전기통신금융사기'
    },
    {
        'question':'은행이 정기예금에 대해 발행하는 무기명 예금증서로 예금자는 이를 금융시장에서 자유로이 매매할 수 있는 것은?',
        'answer':'양도성예금증서'
    },
    {
        'question':'계정과목 또는 금액이 미확정이어서 정당 계정처리가 어려울때 일시 회계처리하는 계정을 뜻하는 것은?',
        'answer':'가수금'
    },
    {
        'question':' 은행, 증권사, 보험회사 등 금융기관으로부터 받은 이자 및 배당 소득이 연간 총액 2천만원 초과시 합산하여 종합소득으로 과세하는 제도는?',
        'answer':'금융소득종합과세'
    },
    {
        'question':'채권이나 증서의 면에 투자가(소유자)의 이름을 기재하고 발행자의 등록부에도 소유자의 성명 및 주소를 등록한 채권증서는?',
        'answer':'기명식'
    },
    {
        'question':'인장을 찍는 행위를 무엇이라 하는가?',
        'answer':'날인'
    },
    {
        'question':'이자를 계산할 때 원금에 대해서만 일정한 시기에 약정한 이율(利率)을 적용하여 계산하는 금리 계산방법은?',
        'answer':'단리'
    },
    {
        'question':'투자원금과 그 이자 및 이자에 대한 이자까지 고려한 이자율 또는 그렇게 계산된 이자나 이자계산방식은?',
        'answer':'복리'
    },
    {
        'question':'수표나 어음등의 지급지가 같은 은행의 같은 지점을 말한다. 다만 자기앞수표의 경우에 같은 은행에서는 어디든지 지급이 가능하므로 같은 은행에서 발행한 것은?',
        'answer':'당점권'
    },
    {
        'question':'당점권이외의 어음, 수표 및 기타증표로서 어음교환에 회부가 가능한 것은?',
        'answer':'타점권'
    },
    {
        'question':'현금이 움직이지 않고 통장에서 통장으로 거래가 되는 경우로, 계좌간 실제로 현금을 주고 받진 않지만 전산상으로는 자금이 움직이는데, 이처럼 현금을 수반하지 않고 자금이 전산상으로 이동하는 거래는?',
        'answer':'대체'
    },
    {
        'question':'약속어음, 당좌수표, 가계수표, 타은행발행 자기앞수표등을 입금한 금액으로서 해당은행에서 아직 현금화처리(결제) 되지 않은 것은?',
        'answer':'미결제타점권'
    },
    {
        'question':'어음ㆍ수표 등 지시증권의 수령인이나 그 후의 소지인이 어음 뒷면의 배서란이나 보전에 배서문언ㆍ피배서인을 적고 배서인이 기명날인이나 서명을 하여 피배서인에게 어음을 교부하는 것은?',
        'answer':'배서'
    },
    {
        'question':'금융기관이 업무과정에서 발생하는 미결제·미정리된 일시적 보관금이나 예수금등 타계정으로 처리하기 부적당한 것을 처리하기 위해 설치한 일시적·편의적 계정으로 자기앞수표 발행대전 등이 해당하는 것은?',
        'answer':'별단예금'
    },
    {
        'question':'은행의 중요한 업무에 대하여 이를 승인한 1명의 책임자에게만 결재를 받는 것이 아니라, 또 다른 책임자1명에게 이중으로 결재받아 그 업무에 대하여 사고를 방지하기 위한 제도는 무엇인가?',
        'answer':'복수결재'
    },
    {
        'question':'우리지점에서 다른 본·지점으로 자금을 보내는것을 뜻하는 용어는?',
        'answer':'전금'
    },
    {
        'question':'전금과는 반대되는 성질을 가지는 것으로서 본지점간 자금의 역청구제도에 대한 용어는?',
        'answer':'역환'
    },
    {
        'question':'국내에 있는 송금인이 외국환은행을 통해 해외의 수취인에게 외화를 송금하는 거래는?',
        'answer':'당발송금'
    },
    {
        'question':'해외에 있는 송금인이 송금한 외화를 국내 외국환은행이 수취인에게 지급하는 거래는?',
        'answer':'타발송금'
    },
    {
        'question':'외국환 매입율(bid rate)과 매도율(offered rate)의 차이는? -한글만 기입하시오 ^^',
        'answer':'스프레드'
    },
    {
        'question':'외국환 거래내용을 세목별로 분류하여 각각의 행위에 코드를 부여하고, 거래시 한국은행 외환전산망에 그 정보를 보고 및 집중시켜 통계자료 및 거래동향에 따른 외환정책 등의 각종지표로 활용하고 있는 것은?',
        'answer':'사유코드'
    },
    {
        'question':'미달러(USD)를 제외한 나머지 외국통화를 의미하는 것은?',
        'answer':'이종통화'
    },
    {
        'question':'대가 없는 증여거래를 일반적으로 의미하는 것은?',
        'answer':'이전거래'
    },
    {
        'question':'외국환거래 시 대한민국 국민이었으나 외국에 귀화하여 외국국적을 취득한 시민권자와 아직 대한민국 국적을 보유한 국민으로서 외국에 영주할 권리만 부여받아 체류하고 있는 영주권자를 칭하는 것은?',
        'answer':'재외동포'
    },
    {
        'question':'대고객 외국환 거래시 적용하는 매매율 산정의 기본이 되는 환율로 일중 수시로 변경고시되는 것은?',
        'answer':'매매기준율'
    },
    {
        'question':'해외송금시 외국환거래법령을 회피하고자 송금인 또는 수취인을 여러명으로 분산하여 송금하는 행위는?',
        'answer':'분산송금'
    },
    {
        'question':'송금은행이 송금환을 수취인에게 지급하도록 지급은행에 지시할 때 사용하는 전문을 의미하는 것은? -약어만 기입하시오 ^^',
        'answer':'P/O'
    },
    {
        'question':'런던의 주요 은행 사이에서 단기 자금운용에 적용되는 금리로, 외국환 거래시 기준금리로 자주 이용되는 것은?',
        'answer':'LIBOR'
    },
    {
        'question':'은행이 고객을 위하여 외국과의 당 ,타발 추심환 업무를 수행함에 있어, 당해 거래와 관련한 자금결제과정에 시간차로 인하여 발생하게 되는 일정기간 동안의 부담 비용을 커버할 목적으로 징수하는 이자 형식의 수수료는?',
        'answer':'환가료'
    },
    {
        'question':'은행 등 금융기관의 국제 금융거래에 관한 메세지 송,수신을 위하여 설립된 통신 네트워크는?',
        'answer':'SWIFT'
    },
    {
        'question':'우리은행의 SWIFT CODE를 기입하시오',
        'answer':'HVBKKRSEXXX'
    },
    {
        'question':'외화와 원화가 교환대는 거래로, 거래시 환율이 개입되며 외환매매익이 발생하는 것은?',
        'answer':'포지션 거래'
    },
    {
        'question':'대고객 외국환거래시 외화현찰을 취급하나 포지션이 발생하지 않는 경우 비용보전 차원에서 받는 수수료는?',
        'answer':'현찰수수료'
    },
    {
        'question':'원화를 대가로 한 교환거래 없이 동종의 외국환으로 입,지급이 발생되는 거래는?',
        'answer':'외화대체거래'
    },
    {
        'question':'대고객 외국환 거래시 원화대가를 수반하지 않고 동종의 외국환을 대체되는 경우에 받는 수수료는?',
        'answer':'대체료'
    },
    {
        'question':'무역거래에 있어 은행이 수입상을 대신하여 수출상의 일치하는 제시에 대해 무역대금의 결제를 확약하는 문서는?',
        'answer':'신용장'
    },
    {
        'question':'무역거래에서 운송 화물의 수령 또는 선적을 인증하고, 그 물품의 인도청구권을 문서화한 증권은? -한글만 기입하시오 ^^',
        'answer':'선하증권'
    },
    {
        'question':'수출상과 수입상간 매매계약의 이행을 입증하는 물품명세서, 대금청구서의 역할을 하는 서류는?',
        'answer':'상업송장'
    },
    {
        'question':'대출금이 기한전에 상환됨으로서 대출취급시 발생한 업무원가를 잔여기간에 대하여 보전받고, 재투자위험을 보상받는 수수료를 말하는 것은?',
        'answer':'중도상환해약금'
    }
]

# 문제와 보기 순서를 랜덤하게 섞는 함수
def shuffle_questions(questions):
    for question in questions:
        if 'choices' in question:
            random.shuffle(question['choices'])

def get_wrong_answers(questions, user_answers):
    wrong_answers = []
    for index, question in enumerate(questions):
        user_answer = user_answers.get(question['question'])
        if 'choices' in question:  # 객관식 퀴즈인 경우
            if user_answer != question['answer']:
                wrong_answers.append({'question': question['question'], 'answer': question['answer'], 'choices': question['choices']})
        else:  # 주관식 퀴즈인 경우
            if user_answer.lower() != question['answer'].lower():
                wrong_answers.append({'question': question['question'], 'answer': question['answer']})
    return wrong_answers

@app.route('/')
def quiz():
    multiple_choice = multiple_choice_questions[:]  # 객관식 퀴즈 복사하여 새로운 리스트 생성
    open_ended = open_questions[:]  # 주관식 퀴즈 복사하여 새로운 리스트 생성
    
    shuffle_questions(multiple_choice)  # 객관식 퀴즈 문제와 보기 순서 랜덤화
    random.shuffle(open_ended)  # 주관식 퀴즈 문제 순서 랜덤화
    
    return render_template('quiz.html', multiple_choice=multiple_choice[:43], open_ended=open_ended[:43])

@app.route('/result', methods=['POST'])
def result():
    user_answers = request.form  # 사용자의 답안을 가져옴

    mc_wrong_answers = get_wrong_answers(multiple_choice_questions[:43], user_answers)
    open_wrong_answers = get_wrong_answers(open_questions[:43], user_answers)

    score_mc = len(multiple_choice_questions[:43]) - len(mc_wrong_answers)
    score_open = len(open_questions[:43]) - len(open_wrong_answers)
    total_questions = len(multiple_choice_questions[:43]) + len(open_questions[:43])
    total_correct = score_mc + score_open
    correct_ratio = total_correct / total_questions * 100 if total_questions > 0 else 0

    congrats_message = ""
    if total_questions > 0:
        if correct_ratio < 10:
            congrats_message = "당신은 연천이 어울립니다. 연천의 겨울 체감 온도를 아시나요? 당장 펜을 내려놓고 유니클로 히트텍을 사러가세요."
        elif 10 <= correct_ratio < 30:
            congrats_message = "당신은 수도권을 만만하게 여기고 있습니다. 동두천으로 출근해서 한국인보다 외국인을 더 많이 보고싶다면 이대로 있는 것도 나쁘지 않겠군요."
        elif 30 <= correct_ratio < 50:
            congrats_message = "당신은 발전 가능성이 있습니다! 치안은 나쁘지만 서울과 가까운 안산 정도라면 어떨까요? 호신용품을 검색하세요!"
        elif 50 <= correct_ratio < 70:
            congrats_message = "이정도라면 서울 외곽은 가능성이 있습니다. 태릉 인근에서 밭과 과수원이 함께하는 은행 생활은 정신 건강에 도움이 될 것입니다."
        elif 70 <= correct_ratio < 90:
            congrats_message = "거의 다 왔습니다! 당신의 노력은 당신이 원하는 지점까지 가는 발판이 되어가고 있습니다. 서로 존중할 줄 아는 지성인들을 고객으로 맞이할 가능성이 높습니다!"
        else:
            congrats_message = "당신은 실로 빛나는 지성의 별입니다. 이대로만 연수 일정을 마무리한다면 우리은행에 가지 못할 곳은 없을 것입니다. 졸업 축하드립니다."

    return render_template('result.html', score_mc=score_mc, score_open=score_open,
                           mc_wrong_answers=mc_wrong_answers, open_wrong_answers=open_wrong_answers,
                           congrats_message=congrats_message)
# 이하 템플릿 코드는 변경하지 않아도 됩니다.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050',debug=True)