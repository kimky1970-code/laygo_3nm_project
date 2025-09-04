import laygo2
import laygo2.object
import laygo2.object.database
import laygo2.object.grid
import yaml

# 1. 기술 및 템플릿 라이브러리 로드 (변경 없음)
with open("tech_3nm.yaml", "r") as f:
    tech_params = yaml.load(f, Loader=yaml.FullLoader)
tech = laygo2.technology.Technology(params=tech_params)
from templates_3nm import lib as tlib

# 2. 설계 파라미터 정의 (변경 없음)
w_nmos = 40
nf_nmos = 3
w_pmos = 40
nf_pmos = 1
pn_space = 32

# 3. 레이아웃 설계 시작 (변경 없음)
lib = laygo2.object.database.Library(name="logic_3nm")
dsn = laygo2.object.design.Design(name="inv_3nm", libname="logic_3nm")
dsn.use_library(lib)
dsn.use_library(tlib)

# 4. 소자 인스턴스 생성 (이전과 동일)
nmos_template = tlib.get_template("nmos_fast")
pmos_template = tlib.get_template("pmos_fast")
nmos = nmos_template.generate(name="NMOS", params={"w": w_nmos, "nf": nf_nmos})
pmos = pmos_template.generate(name="PMOS", params={"w": w_pmos, "nf": nf_pmos})

# 5. 소자 배치 (수정됨)
# 5-1. 파워 레일 (MBPR)을 dsn.route()를 사용해 생성 (결정적인 수정)
# 이렇게 하면 vdd_rail과 vss_rail 객체에 핀이 생깁니다.
pg = dsn.pins.get_pin("placement_grid") # 셀 경계 그리드 가져오기
vdd_rail = dsn.route(gridname="routing_M0A_MBPR", mn=[pg.mn[0,1], pg.mn[1,1]])
vss_rail = dsn.route(gridname="routing_M0A_MBPR", mn=[pg.mn[0,0], pg.mn[1,0]])

# 5-2. 트랜지스터 배치
dsn.place(nmos, mn=[[20, 0], [0, 0]]) # x좌표를 20으로 옮겨 레일과 겹치지 않게 함
pmos_y = nmos.bbox[1][1] + pn_space
dsn.place(pmos, mn=[[20, pmos_y], [0, 0]])

# 6. 배선 연결 (Routing) - (수정됨)
# 6-1. 입력 (Gate 연결)
g_route = dsn.route(gridname="routing_GCON_M0A", mn=[nmos.pins["G"].mn[0], pmos.pins["G"].mn[0]])

# 6-2. 출력 (Drain 연결)
d_route = dsn.route(gridname="routing_M0A_M1", mn=[nmos.pins["D"].mn[0], pmos.pins["D"].mn[0]])

# 6-3. 파워 연결 (Source to Rail)
# 이제 파워 레일의 핀(pins[0])에 정상적으로 연결할 수 있습니다.
dsn.route(gridname="routing_M0A_MBPR", mn=[nmos.pins["S"].mn[0], vss_rail.pins[0].mn[0]])
dsn.route(gridname="routing_M0A_MBPR", mn=[pmos.pins["S"].mn[0], vdd_rail.pins[0].mn[0]])

# 7. 핀(Pin) 생성 (수정됨)
dsn.pin(name="IN", gridname="routing_GCON_M0A", pin_obj=g_route.pins[0])
dsn.pin(name="OUT", gridname="routing_M0A_M1", pin_obj=d_route.pins[0])
dsn.pin(name="VDD", gridname="routing_M0A_MBPR", pin_obj=vdd_rail.pins[0])
dsn.pin(name="VSS", gridname="routing_M0A_MBPR", pin_obj=vss_rail.pins[0])

# 8. 생성된 레이아웃을 GDS 파일 및 이미지로 저장 (변경 없음)
dsn.export_to_gds("inv_3nm.gds")
dsn.export_to_mpl("inv_3nm.png")

print("인버터 레이아웃 생성이 완료되었습니다: inv_3nm.gds, inv_3nm.png")