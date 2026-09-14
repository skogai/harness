"""maker_checker_graph.py — 用 LangGraph 实现 maker-checker 图的完整骨架。

对应 Lecture 14「从零构建你的第一张图」的六步：
1. 定义共享状态（State）    2. 列节点     3. 连边
4. 写路由规则              5. 挂 checkpointer   6. 跑图

依赖：pip install langgraph
agent 节点（research/implement/verify）里的模型调用需要你自己接上，
这里留了骨架和调用示意。
"""

from typing import Annotated, TypedDict
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# ---------- 第一步：定义共享状态 ----------

class GraphState(TypedDict):
    requirements: str                              # 需求，研究节点写入
    code: str                                      # 代码，实现节点写入
    review: str                                    # 审查结论：pass / fail / unclear
    attempts: Annotated[int, operator.add]         # 重试次数，用加号合并


# ---------- 第二步：列节点 ----------

def call_model(system: str, content: str) -> str:
    """模型调用示意——接入你自己的 provider（Anthropic / OpenAI / ...）。"""
    raise NotImplementedError("把这里换成真实的模型调用")


def research(state: GraphState) -> dict:
    # agent 节点：定位问题，产出需求说明
    requirements = call_model("你是需求分析 agent", f"分析这个问题：{state.get('requirements', '')}")
    return {"requirements": requirements}


def implement(state: GraphState) -> dict:
    # agent 节点：写代码 + 测试
    code = call_model("你是实现 agent", f"根据需求写代码：{state['requirements']}")
    return {"code": code}


def tests_pass(code: str) -> bool:
    """确定性检查：跑测试。这里用占位逻辑，真实场景执行 pytest 等。"""
    return "def test" in code  # 占位：代码里包含测试才算通过


def verify(state: GraphState) -> dict:
    # agent 节点：独立审查 + 跑测试（注意：不能和实现共用同一个 context）
    review = call_model("你是独立审查 agent", f"审查这段代码：{state['code']}")
    passed = tests_pass(state["code"])
    verdict = "pass" if passed and "通过" in review else "fail"
    return {"review": verdict}


def merge(state: GraphState) -> dict:
    # 确定性节点：commit
    print(f"合并代码（第 {state['attempts']} 次尝试后通过）")
    return {}


# ---------- 第四步：写路由规则（最关键的一步） ----------

def route_after_verify(state: GraphState) -> str:
    if state["review"] == "fail":
        return "implement"      # 验证失败 → 回到实现
    return "merge"              # 验证通过 → 合并


# ---------- 第三步：连边 ----------

graph = StateGraph(GraphState)
graph.add_node("research", research)
graph.add_node("implement", implement)
graph.add_node("verify", verify)
graph.add_node("merge", merge)

graph.add_edge(START, "research")
graph.add_edge("research", "implement")
graph.add_edge("implement", "verify")
graph.add_conditional_edges(
    "verify",
    route_after_verify,
    {"implement": "implement", "merge": "merge"},
)
graph.add_edge("merge", END)


# ---------- 第五步：编译并挂上 checkpointer ----------
# checkpointer 让状态每一步落盘：进程挂了能从断点接着跑，不从头再来。

app = graph.compile(checkpointer=MemorySaver())


# ---------- 第六步：跑图 ----------
# 每次运行传一个 thread_id，checkpointer 靠它区分不同的运行实例。

if __name__ == "__main__":
    result = app.invoke(
        {"requirements": "修复登录页 bug", "attempts": 0},
        config={"configurable": {"thread_id": "session-1"}},
    )
    print(result)
