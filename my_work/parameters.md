# Parameters

*One row per decision your instruction leaves open. Filled in during session 2, with the agent.*

| Parameter | From which phrase | Range | Default | Why this range |
|---|---|---|---|---|
| 结构：扇形，不以平行为准<br>Structure: fan, not parallel | "two opposing fan shapes" / "parallel thin lines" | 锁定为扇形<br>Locked to fan | 两个相对扇形<br>Two opposing fans | （尚未说明）<br>(not yet stated) |
| 相邻夹角：相对前一条累加<br>Step angle: cumulative from previous line | "each line rotating 5 degrees to the right" | 单点 5°（范围未定）<br>Point value 5° (range unset) | 5° | （尚未说明）<br>(not yet stated) |
| 线的总条数<br>Total number of lines | 指令未写数量；课上补问<br>Count never stated; asked in session | 单点 30（范围未定）<br>Point value 30 (range unset) | 30（上 15 + 下 15）<br>30 (15 upper + 15 lower) | （尚未说明）<br>(not yet stated) |
| 上下分组<br>Split between the two fans | "two groups" / "from above and below" | 锁定 上15 / 下15<br>Locked 15 / 15 | 15 / 15 | （尚未说明）<br>(not yet stated) |
| 最短与最长的比<br>Shortest-to-longest ratio | "gradually increase in length and then decrease again" | 最短 = 最长的一半<br>Shortest = half of longest | 0.5 | （尚未说明）<br>(not yet stated) |
| 下扇方向<br>Lower fan | "upper section" 未规定下半；课上补问<br>Lower half unspecified; asked in session | 另一组同样规则往下扇（不是镜像）<br>Same rule, fanning down (not a mirror) | 独立下扇 / 贯穿线<br>Independent downward / through-lines | （尚未说明）<br>(not yet stated) |
| 最长线相对纸高<br>Longest line vs page height | 课上补问<br>Asked in session | 单点 1/3（范围未定）<br>Point value 1/3 (range unset) | 纸高的 1/3<br>1/3 of page height | （尚未说明）<br>(not yet stated) |
| 长度峰值位置<br>Where length peaks | "gradually increase in length and then decrease again" | 一组里中间最长、两头最短<br>Middle of the set longest; ends shortest | 组内中间<br>Mid-group | （尚未说明）<br>(not yet stated) |
| 中间结构<br>Middle structure | "narrow, interwoven" / "twisted ribbon"；学生看图后改定<br>revised after the reference drawing | 锁定：扭曲的腰，不是点；线从一面穿到另一面<br>Locked: twisted waist, not a point; lines pass from one face to the other | 直纹扭转 / ruled twist | 学生原话：扭曲的绳子或扭曲的布（从一面到另一面），连接处不是一个点 |
| 腰宽<br>Waist width | 指令写交织/扭转，未写多宽；对照参考图<br>width unspecified; taken from the reference drawing | 技术滑条 0–120 mm（认账范围未定）<br>technical 0–120 mm (claimed range unset) | 72 mm（为了能看出扭转，请改）<br>72 mm (so the twist is visible; change it) | （尚未说明）<br>(not yet stated) |

**The last column is yours, in your own words.** If you cannot say why, that is a decision you have not actually made yet.

---

## Things the instruction never mentioned at all

*The interesting ones — decisions you did not notice you were making.*

- 线的总条数（已暂定为 30，理由未写）
- Total line count (provisionally 30, reason unwritten)

学生拒绝了「汇于一点的两个扇形」。中间改为扭转的腰。线粗、颜色仍未定。腰宽 36 mm 只是对照参考图的量级，不是你认账的范围。

Not yet decided: how the middle weaves, weight, colour. Angle, count, and longest-ratio are still point values (slider ends are technical limits, not your claimed range). “Disconnected” is implemented as separate line segments; endpoints may meet at the centre (gap 0). If disconnected means they must not touch, move inner gap off 0.

---

## The three regions

**Boring** — where changes to the parameters change nothing you care about.

**Surprising** — where it stopped resembling what you imagined but is still a legitimate execution.

**Breaking point** — where it stops being a valid execution of your instruction at all.

---

## What I rejected, and why

- 拒绝第一版工具：上下扇形在纸心交于一点。原因：想做的是扭曲的绳子/布（从一面到另一面），连接处是扭曲，不是一个点。
- 拒绝 Version 4（左四翻转 + 右三拉长）。原因：回退到上一步，这个新的不要了。
