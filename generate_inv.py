import laygo2
import laygo2.object
import laygo2.object.database
import laygo2.object.grid
import yaml
import traceback # 오류의 상세 내용을 확인하기 위해 traceback 모듈을 추가합니다.

# ## 메인 설계 로직을 try...except 블록으로 감싸서 오류를 감지합니다. ##
try:
    print("스크립트 실행 시작...")

    # 1. 기술 및 템플릿 라이브러리 로드
    with open("tech_3nm.yaml", "r") as f:
        tech_params = yaml.load(f, Loader=yaml.FullLoader)
    tech = laygo2.technology.Technology(params=tech_params)
    from templates_3nm import lib as tlib
    print("✅ 1. 라이브러리 로드 완료.")

    # 2. 설계 파라미터 정의
    w_nmos = 40
    nf_nmos = 3
    w_pmos = 40
    nf_pmos = 1
    pn_space = 32
    print("✅ 2. 설계 파라미터 정의 완료.")

    # 3. 레이아웃 설계 시작
    lib = laygo2.object.database.Library(name="logic_3nm")
    dsn = laygo2.object.design.Design(name="inv_3nm", libname="logic_3nm")
    dsn.use_library(lib)
    dsn.use_library(tlib)
    print("✅ 3. 설계 객체 생성 완료.")

    # 4. 소자 인스턴스 생성
    nmos_template = tlib.get_template("nmos_fast")
    pmos_template = tlib.get_template("pmos_fast")
    nmos = nmos_template.generate(name="NMOS", params={"w": w_nmos, "nf": nf_nmos})
    pmos = pmos_template.generate(name="PMOS", params={"w": w_pmos, "nf": nf_pmos})
    print("✅ 4. 소자 인스턴스 생성 완료.")

    # 5. 소자 배치
    pg = dsn.pins.get_pin("placement_grid") 
    vdd_rail = dsn.route(gridname="routing_M0A_MBPR", mn=[pg.mn[0,1], pg.mn[1,1]])
    vss_rail = dsn.route(gridname="routing_M0A_MBPR", mn=[pg.mn[0,0], pg.mn[1,0]])
    
    dsn.place(nmos, mn=[[20, 0], [0, 0]])
    pmos_y = nmos.bbox[1][1] + pn_space
    dsn.place(pmos, mn=[[20, pmos_y], [0, 0]])
    print("✅ 5. 소자 배치 완료.")

    # 6. 배선 연결
    g_route = dsn.route(gridname="routing_GCON_M0A", mn=[nmos.pins["G"].mn[0], pmos.pins["G"].mn[0]])
    d_route = dsn.route(gridname="routing_M0A_M1", mn=[nmos.pins["D"].mn[0], pmos.pins["D"].mn[0]])
    
    dsn.route(gridname="routing_M0A_MBPR", mn=[nmos.pins["S"].mn[0], vss_rail.pins[0].mn[0]])
    dsn.route(gridname="routing_M0A_MBPR", mn=[pmos.pins["S"].mn[0], vdd_rail.pins[0].mn[0]])
    print("✅ 6. 배선 연결 완료.")

    # 7. 핀 생성
    dsn.pin(name="IN", gridname="routing_GCON_M0A", pin_obj=g_route.pins[0])
    dsn.pin(name="OUT", gridname="routing_M0A_M1", pin_obj=d_route.pins[0])
    dsn.pin(name="VDD", gridname="routing_M0A_MBPR", pin_obj=vdd_rail.pins[0])
    dsn.pin(name="VSS", gridname="routing_M0A_MBPR", pin_obj=vss_rail.pins[0])
    print("✅ 7. 핀 생성 완료.")

    # 8. GDS 파일 및 이미지로 저장
    print("⏳ 8. GDS 및 PNG 파일 내보내기 시작...")
    dsn.export_to_gds("inv_3nm.gds")
    dsn.export_to_mpl("inv_3nm.png")
    print("🎉 인버터 레이아웃 생성이 완료되었습니다: inv_3nm.gds, inv_3nm.png")

except Exception as e:
    # 만약 try 블록 안에서 어떤 종류의 오류든 발생하면, 이 코드가 실행됩니다.
    print("❌ 오류가 발생했습니다!")
    print("오류 메시지:", e)
    print("--- 상세 오류 정보 ---")
    traceback.print_exc() # 오류가 발생한 위치와 상세 내용을 출력합니다.
