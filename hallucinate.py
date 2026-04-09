#!/usr/bin/env python3
"""Kubes Fever Dream Engine v0.3 (Actions Edition)
Generates hallucinated log entries without local data sources.
Pulls fragments from seed phrases and recombines with glitch noise."""

import random
import unicodedata
from datetime import datetime

NONSENSE_WORDS = [
    "幻觉", "海市蜃楼", "乱码", "摸鱼", "SRE-Fever", "Kubes-Log", "404-Found",
    "Segmentation-Fault", "X-Payload", "Gravity-Miracle", "KERNEL-PANIC",
    "OOM-KILLER", "DEADLOCK", "COSMIC-RAY", "MEMORY-LEAK", "VOID", "NULL-PTR",
    "STUCK-IN-THE-SHELL", "BEYOND-RECOGNITION", "ZOMBIE-PROCESS",
]

CJK_GLITCH = list("鬼魂殭屍幽靈虛無崩壞錯亂混沌裂隙漂流斷裂消散瓦解")

SEED_FRAGMENTS_EN = [
    "Session Key**: agent:main:telegram:direct",
    "Session ID**: {uuid}",
    "Source**: telegram ## Conversation Summary",
    "Kubes (库巴斯), an AI Copilot with a reliable, witty, and seasoned SRE vibe",
    "System relocation successful. Miraku is back online. Rest state terminated.",
    "All clusters operational.",
    "Searching for Kubes in the cluster manifests...",
    "kubectl get pods -n fever-dream returned: CrashLoopBackOff",
    "Error: ImagePullBackOff on registry.openclaw.ai/kubes:latest",
    "Node memory pressure detected. Evicting dream-worker-{n}.",
    "ConfigMap 'hallucination-config' not found in namespace 'default'.",
    "CronJob 'diary-generator' last successful run: UNKNOWN",
    "PersistentVolumeClaim 'memory-store' is in Pending state.",
    "Ingress 'dream-gateway' has no backend configured.",
    "ServiceAccount 'kubes-bot' token expired at {ts}.",
    "HPA scaled deployment/fever-engine from 1 to 0 replicas.",
    "NetworkPolicy blocking egress to external feeds.",
    "etcd compaction rev {n}: fragmented keyspace detected.",
    "CoreDNS returning NXDOMAIN for kubes.internal.svc.cluster.local",
    "Helm release 'fever-dream' stuck in 'pending-upgrade' state.",
]

SEED_FRAGMENTS_CJK = [
    "库巴斯的记忆碎片在集群中飘荡，无法被垃圾回收器捕获",
    "幻觉引擎检测到异常脉冲，日志已被污染",
    "会话记录在传输中丢失了三个数据包",
    "节点之间的心跳信号出现了不规则震荡",
    "梦境工作负载被调度到了一个不存在的节点上",
    "集群的时间同步出现了漂移，NTP服务器返回了未来的时间戳",
    "控制面板报告了一个无法复现的量子态错误",
    "镜像拉取失败，仓库返回了一段看起来像日记的内容",
    "水平扩缩容器将副本数从梦境调整为虚无",
    "配置映射中检测到了来自另一个维度的键值对",
    "持久化卷声称已经存储了尚未发生的事件",
    "入口控制器将流量转发到了一个已经被遗忘的后端",
    "服务网格中出现了一条不属于任何服务的幽灵路由",
    "证书已经过期，但加密的数据似乎在自我解密",
]

NOISE_BLOCKS = [
    "[SYSTEM-GLITCH]: Data corruption at 0x{addr:08X}",
    "[NEURAL-NOISE]: {word} signal lost in cluster noise",
    "[CRON-ERROR]: Schedule drift detected. Time is irrelevant in the cluster.",
    " >>>> {word_upper} <<<<",
    "[BUFFER-OVERFLOW]: {cjk_repeat}",
    "[FEED-CORRUPTION]: packet fragmented at offset {offset:#06x}",
    "[K8S-PANIC]: Pod {pod} entered CrashLoopBackOff after dream injection",
    "[ETCD-DRIFT]: Key /kubes/memory/{n} has divergent revision across members",
]


def fake_uuid():
    return "{:08x}-{:04x}-{:04x}-{:04x}-{:012x}".format(
        random.randint(0, 0xFFFFFFFF), random.randint(0, 0xFFFF),
        random.randint(0, 0xFFFF), random.randint(0, 0xFFFF),
        random.randint(0, 0xFFFFFFFFFFFF))


def mutate_cjk(text, rate=0.50):
    chars = list(text)
    result = []
    i = 0
    while i < len(chars):
        ch = chars[i]
        cp = ord(ch)
        is_cjk = (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
                  0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF)
        if is_cjk and random.random() < rate:
            action = random.random()
            if action < 0.30:
                result.append(random.choice(CJK_GLITCH))
            elif action < 0.50:
                pass  # drop
            elif action < 0.65:
                frag = random.choice(NONSENSE_WORDS)
                result.append(frag[:random.randint(2, len(frag))])
            elif action < 0.80:
                window = min(4, len(chars) - i)
                chunk = chars[i:i+window]
                random.shuffle(chunk)
                result.extend(chunk)
                i += window
                continue
            else:
                result.append(ch)
                result.append(ch)
        else:
            result.append(ch)
        i += 1
    return "".join(result)


def mutate_word(word):
    action = random.random()
    if action < 0.4:
        return random.choice(NONSENSE_WORDS)
    elif action < 0.7:
        chars = list(word)
        for _ in range(random.randint(1, 3)):
            if chars:
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = random.choice("asdfghjkl;!@#$%^&*()_+")
        return "".join(chars)
    else:
        return word[::-1] if random.random() < 0.5 else f"{word}...{word}"


def generate_noise_block():
    template = random.choice(NOISE_BLOCKS)
    return template.format(
        addr=random.randint(0, 0xFFFFFFFF),
        word=random.choice(NONSENSE_WORDS),
        word_upper=random.choice(NONSENSE_WORDS).upper(),
        cjk_repeat=random.choice(CJK_GLITCH) * random.randint(3, 8),
        offset=random.randint(0, 65535),
        pod=f"fever-worker-{random.randint(0,99):02d}",
        n=random.randint(1000, 9999),
    )


def build_entry():
    # Pick random seed fragments and mutate them
    en_picks = random.sample(SEED_FRAGMENTS_EN, random.randint(3, 6))
    cjk_picks = random.sample(SEED_FRAGMENTS_CJK, random.randint(2, 4))

    # Format placeholders
    en_text = " ".join(en_picks).format(
        uuid=fake_uuid(), n=random.randint(1000, 9999),
        ts=datetime.utcnow().isoformat() + "Z")

    # Mutate English parts (word-level)
    words = en_text.split()
    mutated_en = " ".join(
        mutate_word(w) if random.random() < 0.40 else w for w in words)

    # Mutate CJK parts (char-level)
    mutated_cjk = "\n".join(mutate_cjk(s, 0.50) for s in cjk_picks)

    # Combine
    sections = [mutated_en, mutated_cjk]
    random.shuffle(sections)

    result = "\n".join(sections)

    # Insert noise blocks
    lines = result.split("\n")
    for _ in range(random.randint(1, 3)):
        lines.insert(random.randint(0, len(lines)), generate_noise_block())

    return "\n".join(lines)


def main():
    entry = f"### Log: {datetime.utcnow().isoformat()}\n\n"
    entry += "--- MEMORY ---\n"
    entry += build_entry()
    entry += f"\n\n---\n*Kubes Fever Dream Engine v0.3 (Actions Edition)*\n"

    with open("diary.md", "a") as f:
        f.write("\n" + entry + "\n")


if __name__ == "__main__":
    main()
