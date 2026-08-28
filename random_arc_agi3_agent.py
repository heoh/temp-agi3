#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "arc-agi>=0.9.2",
# ]
# ///

"""ARC-AGI-3에서 무작위 행동을 수행하는 가장 작은 에이전트 예제.

실행:
    uv run random_arc_agi3_agent.py --game ls20 --steps 100

선택 사항: ARC_API_KEY 환경 변수를 설정하면 등록된 API 키를 사용한다.
"""

import argparse
import random

import arc_agi
from arcengine import GameState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARC-AGI-3 random agent")
    parser.add_argument("--game", default="ls20", help="게임 ID (기본값: ls20)")
    parser.add_argument("--steps", type=int, default=100, help="최대 행동 횟수")
    parser.add_argument("--seed", type=int, help="난수 시드")
    parser.add_argument(
        "--render-mode",
        default="terminal-fast",
        choices=("terminal", "terminal-fast", "human"),
        help="렌더링 방식 (기본값: terminal-fast)",
    )
    return parser.parse_args()


def random_action_data(action: object, rng: random.Random) -> dict[str, int]:
    """복합 행동(예: 클릭)에만 64x64 화면 좌표를 제공한다."""
    if action.is_complex():
        return {"x": rng.randint(0, 63), "y": rng.randint(0, 63)}
    return {}


def main() -> None:
    args = parse_args()
    if args.steps < 1:
        raise SystemExit("--steps must be at least 1")

    rng = random.Random(args.seed)
    arcade = arc_agi.Arcade()
    env = arcade.make(args.game, render_mode=args.render_mode)
    if env is None:
        raise SystemExit(f"Could not create game: {args.game}")

    for step in range(1, args.steps + 1):
        action = rng.choice(env.action_space)
        observation = env.step(action, data=random_action_data(action, rng))

        if observation is None:
            print(f"step {step}: no observation returned")
            break
        if observation.state == GameState.WIN:
            print(f"step {step}: WIN")
            break
        if observation.state == GameState.GAME_OVER:
            print(f"step {step}: GAME_OVER; resetting")
            env.reset()

    scorecard = arcade.get_scorecard()
    if scorecard is not None:
        print(f"final score: {scorecard.score}")


if __name__ == "__main__":
    main()
