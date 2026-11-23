// Motion-Bausteine (kanal-neutral). Aussehen kommt aus ./theme.tsx. Zeitpunkte = Sounds im Python-Adapter (motion_fx.py)!
import React, {useMemo} from "react";
import {AbsoluteFill, interpolate, useCurrentFrame, random, Easing} from "remotion";
import {geoNaturalEarth1, geoMercator, geoPath, geoCentroid} from "d3-geo";
import {feature} from "topojson-client";
// @ts-ignore
import world from "world-atlas/countries-50m.json";
import {s, clamp, ease, Counter, Pop, Glitch, ICONS, useSpring, fmt} from "./lib";
import {T} from "./theme";

const W = 1920, H = 1080;
// @ts-ignore
const feats: any[] = (feature(world, world.objects.countries) as any).features.filter((d: any) => d.id !== "010");
const byId = (id: string) => feats.find((d) => d.id === id);
export const Icon: React.FC<{name: string; size?: number; color?: string}> = ({name, size = 90, color}) => {
  const st = {fill: "none", stroke: color || T.c.ink, strokeWidth: T.iconStroke, strokeLinecap: "round" as const, strokeLinejoin: "round" as const};
  const set: any = (T as any).icons || {}; const fn = set[name] || ICONS[name] || set.doc || ICONS.doc;
  return <svg width={size} height={size} viewBox="0 0 100 100" style={T.iconFilter ? {filter: T.iconFilter} : undefined}>{fn(st, st.stroke)}</svg>;
};
const Big: React.FC<{at: number; text: string; color?: string; size?: number}> = ({at, text, color, size = 120}) => {
  const sp = useSpring(at); const f = useCurrentFrame();
  if (f < s(at)) return null;
  return <div style={{fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: size, color: color || T.c.ink, lineHeight: 1.02, textTransform: "uppercase",
    transform: `translateY(${(1 - sp) * 40}px)`, opacity: Math.min(1, sp * 1.5), ...T.headStyle}}>{text}</div>;
};
const N = (v: number, at: number, dur: number, p: any = {}) => <Counter to={v} at={at} dur={dur} sep={T.num.sep} decSep={T.num.decSep} {...p} />;

/* ======================= MAP ======================= */
export const MAP_T = {pin: (i: number) => 0.45 + i * 0.55, swarm: [0.2, 1.6], hl: (i: number, n: number) => 0.3 + (i / Math.max(1, n)) * 1.1, counter: 0.4};
export const MapC: React.FC<any> = ({label, title, view = "world", pins = [], threads = "chain", swarm = 0, highlight = [], counter, pulse}) => {
  const f = useCurrentFrame();
  const proj = useMemo(() => {
    if (view === "world") return geoNaturalEarth1().fitExtent([[90, 120], [W - 90, H - 60]], {type: "FeatureCollection", features: feats} as any);
    if (view === "europe") return geoMercator().center([12, 52]).scale(1100).translate([W / 2, H / 2 + 40]);
    return geoMercator().center([view[0], view[1]]).scale(view[2]).translate([W / 2, H / 2 + 40]);
  }, [JSON.stringify(view)]);
  const path = useMemo(() => geoPath(proj), [proj]);
  const ds = useMemo(() => feats.map((d) => ({id: d.id, d: path(d) || ""})), [path]);
  const pts = pins.map((p: any) => proj(p.lonlat || (geoCentroid(byId(p.id)) as any)) as [number, number]);
  const sw = useMemo(() => {
    if (!swarm) return [];
    const big = feats.map((d) => ({c: proj(geoCentroid(d)) as [number, number], a: path.area(d)})).filter((x) => x.c && x.a > 60 && x.c[0] > 0 && x.c[0] < W);
    const tot = big.reduce((a, b) => a + Math.sqrt(b.a), 0);
    return Array.from({length: swarm}).map((_, k) => {
      let r = random(`p${k}`) * tot, pick = big[0];
      for (const b of big) { r -= Math.sqrt(b.a); if (r <= 0) { pick = b; break; } }
      const rad = Math.sqrt(pick.a) * 0.35;
      return {x: pick.c[0] + (random(`x${k}`) - 0.5) * rad, y: pick.c[1] + (random(`y${k}`) - 0.5) * rad, t: random(`t${k}`)};
    });
  }, [swarm, proj, path]);
  const pairs: [number, number][] = threads === "none" ? [] : threads === "chain" ? pins.slice(1).map((_: any, i: number) => [i, i + 1]) : threads;
  return (
    <T.Bg>
      <AbsoluteFill>
        <svg width={W} height={H}>
          <defs><filter id="gl"><feGaussianBlur stdDeviation="4" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter></defs>
          <g style={T.mapFilter ? {filter: T.mapFilter} : undefined}>
          {ds.map((p) => {
            const i = highlight.indexOf(p.id);
            const ho = i >= 0 ? interpolate(f, [s(MAP_T.hl(i, highlight.length)), s(MAP_T.hl(i, highlight.length)) + 8], [0, 1], clamp) : 0;
            return <path key={p.id} d={p.d} fill={ho ? T.c.hl(ho) : T.c.land} stroke={ho ? T.c.hot : T.c.border} strokeWidth={ho ? 1.8 : T.borderW} />;
          })}
          </g>
          {sw.map((p, i) => {
            const at = s(MAP_T.swarm[0]) + p.t * s(MAP_T.swarm[1] - MAP_T.swarm[0]);
            const o = interpolate(f, [at, at + 5], [0, 1], clamp), ring = interpolate(f, [at, at + 14], [0, 1], clamp);
            return <g key={i} opacity={o}><circle cx={p.x} cy={p.y} r={2.8} fill={T.c.dot} filter={T.glow ? "url(#gl)" : undefined} />
              {ring < 1 && <circle cx={p.x} cy={p.y} r={2 + ring * 14} fill="none" stroke={T.c.dot} strokeOpacity={1 - ring} strokeWidth={1.4} />}</g>;
          })}
          {pairs.map(([a, b], k) => {
            if (!pts[a] || !pts[b]) return null;
            const t0 = MAP_T.pin(Math.max(a, b)) - 0.35;
            const pr = interpolate(f, [s(t0), s(t0 + 0.5)], [0, 1], {...clamp, easing: ease});
            return <T.Thread key={k} x1={pts[a][0]} y1={pts[a][1]} x2={pts[b][0]} y2={pts[b][1]} p={pr} />;
          })}
          {pins.map((p: any, i: number) => {
            const t0 = MAP_T.pin(i); if (f < s(t0)) return null;
            const k = interpolate(f, [s(t0), s(t0) + 6], [1.8, 1], {...clamp, easing: ease});
            const pu = ((f - s(t0)) % 24) / 24;
            return <g key={i}>{pulse && <circle cx={pts[i][0]} cy={pts[i][1]} r={12 + pu * 40} fill="none" stroke={T.c.hot} strokeOpacity={1 - pu} strokeWidth={3} />}
              <T.Pin x={pts[i][0]} y={pts[i][1]} k={k} /></g>;
          })}
        </svg>
        {pins.map((p: any, i: number) => p.label && f >= s(MAP_T.pin(i) + 0.15) ? (
          <div key={i} style={{position: "absolute", left: pts[i][0] + 22, top: pts[i][1] + (i % 2 ? 18 : -60), ...T.tag}}>
            <T.Write text={p.label} at={MAP_T.pin(i) + 0.15} style={{fontSize: 30, ...T.tagText}} /></div>) : null)}
      </AbsoluteFill>
      <T.Label text={label} />
      {title && <div style={{position: "absolute", left: 80, top: 130}}><Big at={0.15} text={title} size={100} /></div>}
      {counter && <div style={{position: "absolute", left: 0, right: 0, bottom: 70, display: "flex", justifyContent: "center"}}>
        <div style={{...T.panel, display: "flex", alignItems: "baseline", gap: 22}}>
          <span style={{fontFamily: T.font.num, fontWeight: T.headWeight, fontSize: 104, color: T.c.panelInk}}>{N(counter.value, MAP_T.counter, 1.2, {prefix: counter.prefix, suffix: counter.suffix})}</span>
          <span style={{fontFamily: T.font.body, fontSize: 40, color: T.c.panelAccent, fontWeight: 700}}>{counter.label}</span></div></div>}
    </T.Bg>
  );
};

/* ======================= FLOW ======================= */
export const FLOW_T = {node: (i: number) => 0.1 + i * 0.15, go: 0.6, seg: 0.75, branchAt: (after: number) => 0.6 + 0.75 * (after + 0.5)};
export const FlowC: React.FC<any> = ({label, steps, nodes, packet = "doc", branch, len}) => {
  const f = useCurrentFrame(); const n = nodes.length;
  const xs = nodes.map((_: any, i: number) => 260 + (i * (W - 520)) / Math.max(1, n - 1)); const y = 470;
  const tAll = FLOW_T.go + FLOW_T.seg * (n - 1);
  const g = interpolate(f, [s(FLOW_T.go), s(tAll)], [0, n - 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const seg = Math.min(n - 2, Math.floor(g)); const px = xs[seg] + (xs[seg + 1] - xs[seg]) * (g - seg);
  const prog = interpolate(f, [0, s(len * 0.85)], [0, 1], clamp);
  const bx = branch ? (xs[branch.after] + xs[branch.after + 1]) / 2 : 0; const by = 860;
  const bt = branch ? FLOW_T.branchAt(branch.after) : 0;
  const sp = branch ? interpolate(f, [s(bt), s(bt + 0.8)], [0, 1], {...clamp, easing: ease}) : 0;
  const pk = (x: number, yy: number, hot: boolean) => <g transform={`translate(${x - 40},${yy - 40})`}><foreignObject width={80} height={80}><Icon name={packet} size={80} color={hot ? T.c.hot : T.c.accent} /></foreignObject></g>;
  return (
    <T.Bg>
      <T.Label text={label} />
      {steps && <>
        <div style={{position: "absolute", left: 80, right: 80, top: 150, height: 6, background: T.c.track}}>
          <div style={{width: `${prog * 100}%`, height: "100%", background: T.c.accent, boxShadow: T.glow ? `0 0 12px ${T.c.accent}` : undefined}} /></div>
        {steps.map((t: string, i: number) => <div key={i} style={{position: "absolute", top: 172, left: 80 + i * ((W - 160) / steps.length), fontFamily: T.font.body, fontWeight: 700, fontSize: 26,
          color: prog >= i / steps.length ? T.c.accent : T.c.muted}}>{`0${i + 1}  ${t.toUpperCase()}`}</div>)}
      </>}
      <svg width={W} height={H} style={{position: "absolute"}}>
        {xs.slice(1).map((x: number, i: number) => <line key={i} x1={xs[i] + 110} y1={y} x2={x - 110} y2={y} stroke={T.c.track} strokeWidth={4} strokeDasharray="14 10" />)}
        {branch && <T.Thread x1={bx} y1={y} x2={bx} y2={by - 110} p={sp} straight />}
        {f >= s(FLOW_T.go) && f < s(tAll) && pk(px, y, false)}
        {branch && sp > 0 && pk(bx, y + (by - 150 - y) * sp, true)}
      </svg>
      {nodes.map((nd: any, i: number) => (
        <div key={i} style={{position: "absolute", left: xs[i] - 130, top: y - 110, width: 260, textAlign: "center"}}>
          <Pop at={FLOW_T.node(i)}>{(T as any).Node ? <div style={{margin: "0 auto", width: 220}}>{React.createElement((T as any).Node, {hot: false}, <Icon name={nd.icon} size={100} color={T.c.nodeInk} />)}</div> : <div style={{width: 170, height: 170, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "center", ...T.node}}><Icon name={nd.icon} size={100} color={T.c.nodeInk} /></div>}
            <div style={{fontFamily: T.font.body, fontWeight: 700, fontSize: 30, color: T.c.ink, marginTop: 16}}>{nd.label}</div></Pop>
        </div>))}
      {branch && <div style={{position: "absolute", left: bx - 130, top: by - 110, width: 260, textAlign: "center"}}>
        <Pop at={bt + 0.5}>{(T as any).Node ? <div style={{margin: "0 auto", width: 220}}>{React.createElement((T as any).Node, {hot: true}, <Icon name={branch.icon} size={100} color={T.c.hot} />)}</div> : <div style={{width: 170, height: 170, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "center", ...T.nodeHot}}><Icon name={branch.icon} size={100} color={T.c.hot} /></div>}
          <div style={{fontFamily: T.font.body, fontWeight: 700, fontSize: 30, color: T.c.ink, marginTop: 16}}>{branch.label}</div></Pop></div>}
      {branch && <div style={{position: "absolute", top: by - 60, ...(bx > W * 0.55 ? {right: W - bx + 150, textAlign: "right"} : {left: bx + 150})}}><Big at={bt + 0.7} text={branch.text} color={T.c.hot} size={70} /></div>}
    </T.Bg>
  );
};

/* ======================= FLIP ======================= */
export const FlipC: React.FC<any> = ({teaser, front, back, at = 2.4}) => {
  const f = useCurrentFrame();
  const fl = interpolate(f, [s(at), s(at + 0.3)], [0, 180], {...clamp, easing: Easing.bezier(0.7, 0, 0.3, 1)});
  const tease = interpolate(f, [s(0.2), s(at - 0.1)], [0, 24], {...clamp, easing: Easing.inOut(Easing.sin)});
  const shake = f >= s(at + 0.15) && f < s(at + 0.55) ? (random(`sh${f}`) - 0.5) * 26 : 0;
  return (
    <T.Bg hot={fl > 90}>
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", transform: `translate(${shake}px,${shake * 0.5}px)`}}>
        <div style={{perspective: 2000}}>
          <div style={{width: 620, height: 760, position: "relative", transformStyle: "preserve-3d", transform: `rotateY(${fl > 0 ? fl : tease}deg)`}}>
            <div style={{position: "absolute", inset: 0, backfaceVisibility: "hidden", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 36, ...T.card}}>
              {T.cardTop && <div style={{position: "absolute", top: 34, left: 40, ...T.cardTopStyle}}>{T.cardTop}</div>}
              <Glitch at={at - 0.6}><Icon name={front.icon || "doc"} size={220} color={T.c.cardInk} /></Glitch>
              <div style={{fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: 96, color: T.c.cardInk, textAlign: "center", lineHeight: 1, textTransform: "uppercase"}}>{front.title}</div>
            </div>
            <div style={{position: "absolute", inset: 0, backfaceVisibility: "hidden", transform: "rotateY(180deg)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 22, ...T.cardHot}}>
              <div style={{fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: back.title.length > 5 ? Math.min(130, Math.floor(1000 / back.title.length)) : 190, color: T.c.cardHotInk, lineHeight: 1, textAlign: "center", textTransform: "uppercase"}}>{back.title}</div>
              <div style={{width: 320, height: 5, background: T.c.hot}} />
              {back.sub && <div style={{fontFamily: T.font.body, fontWeight: 700, fontSize: 34, color: T.c.cardHotInk, textAlign: "center", padding: "0 30px"}}>{back.sub}</div>}
            </div>
          </div>
        </div>
      </AbsoluteFill>
      {teaser && <div style={{position: "absolute", left: 90, bottom: 90}}><T.Write text={teaser} at={0.25} style={{fontSize: 44, color: T.c.muted}} /></div>}
    </T.Bg>
  );
};

/* ======================= COUNTER ======================= */
export const CounterC: React.FC<any> = ({label, value, prefix, suffix, dec, caption, items = "none"}) => {
  const f = useCurrentFrame();
  return (
    <T.Bg>
      {items !== "none" && Array.from({length: 36}).map((_, i) => {
        const x = random(`mx${i}`) * 1840; const v = 5 + random(`ms${i}`) * 9; const y = 1150 - ((f * v + random(`my${i}`) * 1400) % 1400);
        const rot = (random(`r${i}`) - 0.5) * 50 + f * (random(`rr${i}`) - 0.5) * 0.6;
        return <div key={i} style={{position: "absolute", left: x, top: y, opacity: 0.3, transform: `rotate(${rot}deg)`}}><Icon name={items} size={110} color={T.c.muted} /></div>;
      })}
      <T.Label text={label} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center"}}>
        <div style={{...T.panel, textAlign: "center", padding: (T as any).counterPad || "26px 70px"}}>
          <div style={{fontFamily: T.font.num, fontWeight: T.headWeight, fontSize: 200, color: T.c.panelInk, lineHeight: 1}}>{N(value, 0.1, 1.6, {prefix, suffix, dec})}</div>
          <Pop at={0.9}><div style={{fontFamily: T.font.body, fontWeight: 700, fontSize: 46, color: T.c.panelAccent, letterSpacing: 3, marginTop: 6}}>{caption}</div></Pop>
        </div>
      </AbsoluteFill>
    </T.Bg>
  );
};

/* ======================= GRID ======================= */
export const GridC: React.FC<any> = ({label, n = 60, icon = "person", value, suffix = "", caption, hot = 9}) => {
  const f = useCurrentFrame();
  return (
    <T.Bg>
      <T.Label text={label} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "row", gap: 90}}>
        <div style={{display: "grid", gridTemplateColumns: "repeat(10, 66px)", gap: 14}}>
          {Array.from({length: n}).map((_, i) => {
            const at = s(T.gridRows ? 0.15 + Math.floor(i / 10) * 0.22 + (i % 10) * 0.025 : 0.15 + random(`o${i}`) * 1.3);
            const p = interpolate(f, [at, at + 7], [0, 1], {...clamp, easing: ease}); const h = hot > 0 && i % hot === Math.min(3, hot - 1);
            return <div key={i} style={{width: 66, height: 66, transform: `scale(${p}) rotate(${(random(`q${i}`) - 0.5) * T.tileJitter}deg)`, opacity: p,
              display: "flex", alignItems: "center", justifyContent: "center", ...((T as any).Tile ? {} : (h ? T.tileHot : T.tile))}}>{(T as any).Tile ? React.createElement((T as any).Tile, {hot: h, icon, i}) : <Icon name={icon} size={50} color={h ? T.c.hot : T.c.tileInk} />}</div>;
          })}
        </div>
        <div>
          <div style={{fontFamily: T.font.num, fontWeight: T.headWeight, fontSize: (fmt(value) + suffix).length > 4 ? 170 : 220, color: T.c.ink, lineHeight: 1.05}}>{N(value, 0.9, 1.0, {suffix})}</div>
          <Pop at={1.6}><div style={{fontFamily: T.font.body, fontWeight: 700, fontSize: 44, color: T.c.accent, maxWidth: 560, marginTop: 18}}>{caption}</div></Pop>
        </div>
      </AbsoluteFill>
    </T.Bg>
  );
};

/* ======================= PHONE ======================= */
export const PhoneC: React.FC<any> = ({label, app = "NACHRICHTEN", messages, quote, len}) => {
  const f = useCurrentFrame(); const tilt = interpolate(f, [0, s(len)], [-16, -4], clamp);
  return (
    <T.Bg>
      <T.Label text={label} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", flexDirection: "row", gap: 110}}>
        <div style={{perspective: 1600}}>
          <div style={{width: 430, height: 860, borderRadius: 60, background: "linear-gradient(145deg,#2d2d30,#0b0b0d)", padding: 14, transform: `rotateY(${tilt}deg)`,
            boxShadow: "0 40px 120px rgba(0,0,0,0.6), inset 0 0 0 2px #45454a", ...((T as any).phoneFrame || {})}}>
            <div style={{width: "100%", height: "100%", borderRadius: 48, background: "#0b0b0c", overflow: "hidden", ...((T as any).phoneScreen || {})}}>
              <div style={{padding: "64px 28px 18px", fontFamily: "Inter, sans-serif", fontWeight: 800, fontSize: 28, color: "#eee", borderBottom: "1px solid #2a2a2a", ...((T as any).phoneHead || {})}}>{app}</div>
              <div style={{display: "flex", flexDirection: "column", gap: 16, padding: "26px 22px"}}>
                {messages.map(([t, me]: [string, boolean], i: number) => {
                  const sp = useSpring(0.15 + i * 0.4);
                  if (f < s(0.15 + i * 0.4)) return <div key={i} />;
                  return <div key={i} style={{alignSelf: me ? "flex-end" : "flex-start", maxWidth: 300, padding: "14px 20px", borderRadius: 22, fontFamily: "Inter, sans-serif", fontSize: 24,
                    background: me ? T.c.bubble : "#26262a", color: "#f2f2f2", ...((T as any).phoneBubble || {}), transform: `translateY(${(1 - sp) * 26}px)`, opacity: Math.min(1, sp * 2)}}>{t}</div>;
                })}
              </div>
            </div>
          </div>
        </div>
        {quote && <div style={{width: 760}}><T.Write text={`„${quote}“`} at={0.15 + messages.length * 0.4} style={{fontSize: 60, color: T.c.ink, lineHeight: 1.2}} /></div>}
      </AbsoluteFill>
    </T.Bg>
  );
};

/* ======================= CIPHER ======================= */
export const CipherC: React.FC<any> = ({label, text, caption}) => {
  const f = useCurrentFrame(); const gl = "A7#Q$9X%K2@M&Z5!F8";
  const size = Math.min(70, Math.floor(1700 / Math.max(10, text.length) / 0.62));
  return (
    <T.Bg>
      <T.Label text={label} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center", gap: 50}}>
        <div style={{display: "flex", justifyContent: "center"}}>
          {text.split("").map((c: string, i: number) => {
            const scr = f > s(0.3 + i * 0.025);
            const ch = c === " " ? " " : scr ? gl[Math.floor(random(`c${i}${Math.floor(f / 2)}`) * gl.length)] : c;
            return <span key={i} style={{fontFamily: T.font.mono, fontSize: size, color: scr ? T.c.hot : T.c.ink, width: size * 0.62, textAlign: "center"}}>{ch}</span>;
          })}
        </div>
        {caption && <Pop at={0.9}><div style={{fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: 64, color: T.c.ink, textTransform: "uppercase"}}>{caption}</div></Pop>}
      </AbsoluteFill>
    </T.Bg>
  );
};

/* ======================= STACK ======================= */
export const StackC: React.FC<any> = ({label, cards, symbol = "?", question}) => {
  const f = useCurrentFrame(); const m = (cards.length - 1) / 2;
  const hy = interpolate(f, [s(1.5), s(1.72), s(1.9)], [-60, 10, 0], {...clamp, easing: ease});
  return (
    <T.Bg>
      <T.Label text={label} />
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center"}}>
        {cards.map(([t, sub]: [string, string], i: number) => {
          const sp = useSpring(0.1 + i * 0.16);
          return <div key={i} style={{position: "absolute", width: 560, height: 320, padding: 32, ...T.sheet,
            transform: `translate(${(i - m) * 48}px, ${(i - m) * -30 + (1 - sp) * 700}px) rotate(${(i - m) * 4}deg)`}}>
            <div style={{fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: 40, color: T.c.sheetInk}}>{t}</div>
            <div style={{fontFamily: T.font.body, fontSize: 26, color: T.c.sheetInk, opacity: 0.7, marginTop: 8}}>{sub}</div>
            <div style={{marginTop: 26, height: 10, width: 420, background: T.c.sheetLine}} /><div style={{marginTop: 12, height: 10, width: 340, background: T.c.sheetLine}} />
          </div>;
        })}
        <div style={{position: "absolute", top: 110, fontFamily: T.font.head, fontWeight: T.headWeight, fontSize: 210, color: T.c.hot, transform: `translateY(${hy}px)`, opacity: f >= s(1.5) ? 1 : 0, ...((T as any).symbolStyle || {})}}>{symbol}</div>
      </AbsoluteFill>
      {question && <div style={{position: "absolute", left: 0, right: 0, bottom: 80, textAlign: "center"}}><T.Write text={question} at={0.6} style={{fontSize: 48, color: T.c.ink}} /></div>}
    </T.Bg>
  );
};

/* ======================= BARS (Vergleich) ======================= */
export const BarsC: React.FC<any> = ({label, title, unit = "", bars}) => {
  const f = useCurrentFrame(); const mx = Math.max(...bars.map((b: any) => b[1]));
  return (
    <T.Bg>
      <T.Label text={label} />
      {title && <div style={{position: "absolute", left: 0, right: 0, top: 150, textAlign: "center"}}><Big at={0.1} text={title} size={80} /></div>}
      <div style={{position: "absolute", left: 220, right: 220, top: 330, display: "flex", flexDirection: "column", gap: 50}}>
        {bars.map(([name, v, hot]: [string, number, boolean], i: number) => {
          const at = 0.4 + i * 0.35; const p = interpolate(f, [s(at), s(at + 0.9)], [0, 1], {...clamp, easing: ease});
          return <div key={i} style={{display: "flex", alignItems: "center", gap: 30}}>
            <div style={{width: 300, textAlign: "right", fontFamily: T.font.body, fontWeight: 700, fontSize: 36, color: T.c.ink}}>{name}</div>
            <div style={{flex: 1, position: "relative", height: 70}}>
              <div style={{position: "absolute", left: 0, top: 0, bottom: 0, width: `${(v / mx) * 100 * p}%`, ...(hot ? T.barHot : T.bar)}} />
            </div>
            <div style={{width: 260, fontFamily: T.font.num, fontWeight: T.headWeight, fontSize: 52, color: hot ? T.c.hot : T.c.ink}}>{N(v, at, 0.9, {suffix: unit, dec: (String(v).split('.')[1] || '').length})}</div>
          </div>;
        })}
      </div>
    </T.Bg>
  );
};
