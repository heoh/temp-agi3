# ARC-AGI-3 최소 랜덤 에이전트

`random_arc_agi3_agent.py`는 매 스텝마다 가능한 행동 중 하나를 무작위로 골라
ARC-AGI-3 게임을 실행하는 최소 예제입니다. 복합 행동에는 0~63 범위의 무작위
`x`, `y` 좌표를 함께 전달합니다.

Python 3.12+와 [uv](https://docs.astral.sh/uv/)가 필요합니다.

```bash
uv run random_arc_agi3_agent.py --game ls20 --steps 100
```

반복 가능한 실행에는 시드를 지정합니다.

```bash
uv run random_arc_agi3_agent.py --game ls20 --steps 100 --seed 42
```

공개 게임 외 환경에 접근하려면 ARC Prize 계정에서 받은 키를 설정합니다.

```bash
export ARC_API_KEY="your-api-key"
uv run random_arc_agi3_agent.py --game ls20
```

`--render-mode terminal`(속도 제한), `terminal-fast`(기본값), `human` 중 하나를
선택할 수 있습니다.
