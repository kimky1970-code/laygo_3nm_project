import laygo2
import laygo2.object
import laygo2.object.database
import laygo2.object.grid

# 템플릿들을 저장할 라이브러리를 생성합니다.
# 이 라이브러리는 NMOS, PMOS 등 여러 템플릿을 담는 컨테이너 역할을 합니다.
lib = laygo2.object.database.TemplateLibrary(name="templates_3nm")

# 1. NMOS 트랜지스터 템플릿 정의
# 'nmos_fast'라는 이름의 템플릿을 생성합니다.
# 이 템플릿은 1x1 크기의 가상 그리드를 기준으로 핀의 상대 위치를 정의합니다.
nmos_template = laygo2.object.template.Template(
    name="nmos_fast",
    libname="templates_3nm",
    gridname="placement_grid", # tech_3nm.yaml에 정의된 그리드 이름
    pins={
        "S": laygo2.object.Pin(xy=[[0, 0], [20, 0]], layer=["M0A", "drawing"], netname="S"),
        "D": laygo2.object.Pin(xy=[[0, 20], [20, 20]], layer=["M0A", "drawing"], netname="D"),
        "G": laygo2.object.Pin(xy=[[-10, 10], [0, 10]], layer=["Gate", "drawing"], netname="G"),
    },
)
# 소자의 실제 경계 영역(Boundary)을 prBoundary 레이어로 정의합니다.
nmos_template.append(
    laygo2.object.Rect(
        xy=[[0, 0], [20, 20]],
        layer=["prBoundary", "drawing"],
    )
)
lib.append(nmos_template) # 라이브러리에 NMOS 템플릿 추가

# 2. PMOS 트랜지스터 템플릿 정의
# 'pmos_fast'라는 이름의 템플릿을 생성합니다.
pmos_template = laygo2.object.template.Template(
    name="pmos_fast",
    libname="templates_3nm",
    gridname="placement_grid", # tech_3nm.yaml에 정의된 그리드 이름
    pins={
        "S": laygo2.object.Pin(xy=[[0, 20], [20, 20]], layer=["M0A", "drawing"], netname="S"),
        "D": laygo2.object.Pin(xy=[[0, 0], [20, 0]], layer=["M0A", "drawing"], netname="D"),
        "G": laygo2.object.Pin(xy=[[-10, 10], [0, 10]], layer=["Gate", "drawing"], netname="G"),
    },
)
# 소자의 실제 경계 영역(Boundary)을 prBoundary 레이어로 정의합니다.
pmos_template.append(
    laygo2.object.Rect(
        xy=[[0, 0], [20, 20]],
        layer=["prBoundary", "drawing"],
    )
)
lib.append(pmos_template) # 라이브러리에 PMOS 템플릿 추가