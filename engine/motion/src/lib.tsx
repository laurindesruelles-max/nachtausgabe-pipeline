// Kanal-neutrale Helfer. Der Kanal-Look kommt ausschliesslich aus ./theme.tsx (pro Kanal eigene Datei).
import React from "react";
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing, random} from "remotion";

export const FPS = 30;
export const s = (t: number) => Math.round(t * FPS);
export const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"} as const;
export const ease = Easing.bezier(0.22, 1, 0.36, 1);

export const useT = (a: number, b: number, e = ease) => interpolate(useCurrentFrame(), [s(a), s(b)], [0, 1], {...clamp, easing: e});
export const useSpring = (at: number, cfg = {damping: 14, mass: 0.6, stiffness: 140}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  return spring({frame: f - s(at), fps, config: cfg});
};
export const fmt = (n: number, dec = 0, sep = ".", decSep = ",") => {
  const v = dec ? n.toFixed(dec) : Math.round(n).toString();
  const [a, b] = v.split("."); return a.replace(/\B(?=(\d{3})+(?!\d))/g, sep) + (b ? decSep + b : "");
};
export const Counter: React.FC<{to: number; at: number; dur?: number; prefix?: string; suffix?: string; dec?: number; sep?: string; decSep?: string; style?: React.CSSProperties}> =
  ({to, at, dur = 1.2, prefix = "", suffix = "", dec = 0, sep, decSep, style}) => {
  const p = useT(at, at + dur, Easing.bezier(0.16, 1, 0.3, 1));
  return <span style={{fontVariantNumeric: "tabular-nums", ...style}}>{prefix}{fmt(to * p, dec, sep, decSep)}{suffix}</span>;
};
export const Pop: React.FC<{at: number; children: React.ReactNode; style?: React.CSSProperties; from?: number}> = ({at, children, style, from = 0.6}) => {
  const sp = useSpring(at); const f = useCurrentFrame();
  if (f < s(at)) return null;
  return <div style={{transform: `scale(${from + (1 - from) * sp})`, opacity: Math.min(1, sp * 1.6), filter: `blur(${(1 - Math.min(1, sp)) * 8}px)`, ...style}}>{children}</div>;
};
export const Drift: React.FC<{len: number; children: React.ReactNode}> = ({len, children}) => {
  const f = useCurrentFrame();
  const i = interpolate(f, [0, 8], [1, 0], {...clamp, easing: ease});
  const sc = interpolate(f, [0, s(len)], [1, 1.04], clamp) * (1 + 0.06 * i);
  return <AbsoluteFill style={{transform: `scale(${sc})`, filter: `blur(${i * 8}px)`}}>{children}</AbsoluteFill>;
};
export const Glitch: React.FC<{at: number; dur?: number; children: React.ReactNode}> = ({at, dur = 0.35, children}) => {
  const f = useCurrentFrame(); const on = f >= s(at) && f < s(at + dur);
  const k = on ? random(`g${f}`) - 0.5 : 0;
  return (
    <div style={{position: "relative", transform: `translateX(${k * 30}px)`}}>
      {on && <div style={{position: "absolute", inset: 0, transform: `translateX(${-k * 18}px)`, filter: "drop-shadow(4px 0 0 rgba(255,60,0,0.8))", opacity: 0.8}}>{children}</div>}
      <div style={{clipPath: on ? `inset(${random(`a${f}`) * 40}% 0 ${random(`b${f}`) * 40}% 0)` : undefined}}>{children}</div>
    </div>
  );
};
/** Linien-Icons; Farbe/Strich kommen vom Theme */
export const ICONS: Record<string, (st: any, c: string) => React.ReactNode> = {
  phone: (st) => <><rect x={28} y={8} width={44} height={84} rx={9} {...st} /><circle cx={50} cy={80} r={3} fill={st.stroke} /></>,
  server: (st) => <>{[12, 40, 68].map((y) => <g key={y}><rect x={12} y={y} width={76} height={22} rx={4} {...st} /><circle cx={74} cy={y + 11} r={4} fill={st.stroke} /></g>)}</>,
  bank: (st) => <><path d="M10 38 L50 12 L90 38 Z" {...st} /><path d="M18 84 H82 M22 44 V76 M40 44 V76 M60 44 V76 M78 44 V76" {...st} /></>,
  factory: (st) => <path d="M10 88 V44 L34 58 V44 L58 58 V24 H76 V88 Z" {...st} />,
  person: (st) => <><circle cx={50} cy={32} r={16} {...st} /><path d="M18 90 C18 64 82 64 82 90" {...st} /></>,
  ship: (st) => <path d="M10 62 H90 L78 84 H22 Z M30 62 V40 H62 V62 M46 40 V22" {...st} />,
  money: (st) => <><rect x={8} y={26} width={84} height={48} rx={6} {...st} /><circle cx={50} cy={50} r={12} {...st} /></>,
  doc: (st) => <path d="M24 8 H62 L78 24 V92 H24 Z M62 8 V24 H78 M34 46 H68 M34 60 H68 M34 74 H56" {...st} />,
  store: (st) => <path d="M12 40 L20 14 H80 L88 40 Z M18 40 V88 H82 V40 M40 88 V62 H60 V88" {...st} />,
  lock: (st) => <><rect x={22} y={44} width={56} height={44} rx={6} {...st} /><path d="M34 44 V30 a16 16 0 0 1 32 0 V44" {...st} /></>,
  eye: (st) => <><path d="M8 50 C28 18 72 18 92 50 C72 82 28 82 8 50 Z" {...st} /><circle cx={50} cy={50} r={12} fill={st.stroke} /></>,
  gavel: (st) => <path d="M30 20 L58 48 M44 6 L72 34 M37 13 L65 41 M51 41 L84 74 M14 92 H58" {...st} />,
  gear: (st) => <><circle cx={50} cy={50} r={14} {...st} /><path d="M50 10 V22 M50 78 V90 M10 50 H22 M78 50 H90 M22 22 L30 30 M70 70 L78 78 M78 22 L70 30 M22 78 L30 70" {...st} /><circle cx={50} cy={50} r={28} {...st} /></>,
  truck: (st) => <><path d="M8 30 H60 V72 H8 Z M60 44 H80 L92 58 V72 H60" {...st} /><circle cx={26} cy={76} r={8} {...st} /><circle cx={76} cy={76} r={8} {...st} /></>,
  crane: (st) => <path d="M30 92 V14 H88 M30 14 L14 30 H30 M30 30 L60 14 M76 14 V44 M70 44 H82 V54 H70 Z M20 92 H44" {...st} />,
  brain: (st) => <path d="M50 18 C36 6 14 16 18 34 C6 42 10 62 22 64 C22 80 40 88 50 76 C60 88 78 80 78 64 C90 62 94 42 82 34 C86 16 64 6 50 18 Z M50 18 V76" {...st} />,
  heart: (st) => <path d="M50 84 C20 62 10 46 18 30 C26 16 44 18 50 32 C56 18 74 16 82 30 C90 46 80 62 50 84 Z" {...st} />,
  clock: (st) => <><circle cx={50} cy={50} r={38} {...st} /><path d="M50 26 V50 L66 60" {...st} /></>,
  car: (st) => <><path d="M10 64 V50 L24 32 H70 L86 50 H92 V64 Z" {...st} /><circle cx={28} cy={66} r={9} {...st} /><circle cx={74} cy={66} r={9} {...st} /></>,
  knife: (st) => <path d="M14 86 L58 42 M58 42 L86 14 C90 30 78 48 64 48 Z M14 86 L24 76" {...st} />,
  badge: (st) => <><path d="M50 8 L84 20 V48 C84 70 66 84 50 92 C34 84 16 70 16 48 V20 Z" {...st} /><path d="M38 50 L48 60 L66 38" {...st} /></>,
};
