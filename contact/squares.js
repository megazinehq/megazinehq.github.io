// The squares for the finger-gun test: small two-ink drawings that move, printed a little out of register like the zine.
// One file, used twice: the inbox Worker (tools/inbox-worker/) draws the real ones and keeps the answer; the contact page
// draws its own only in preview, when there is no Worker. Every drawing faces right in a 64 x 64 box and has two plates:
// c, the colour (flat shapes; fill="B" for the second ink, "P" for bare paper) and k, the black line work.
const K = "#18181B";
const at = (type, values, dur, eased) => `<animateTransform attributeName="transform" type="${type}" values="${values}" dur="${dur}s" repeatCount="indefinite"` +
  (eased ? ` calcMode="spline" keyTimes="0;.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"` : "") + "/>";
const spin = (cx, cy, dur, inner) => `<g>${inner}${at("rotate", `0 ${cx} ${cy};360 ${cx} ${cy}`, dur)}</g>`;
const sway = (cx, cy, deg, dur, inner) => `<g>${inner}${at("rotate", `${-deg} ${cx} ${cy};${deg} ${cx} ${cy};${-deg} ${cx} ${cy}`, dur, true)}</g>`;
const bob = (dx, dy, dur, inner) => `<g>${inner}${at("translate", `0 0;${dx} ${dy};0 0`, dur, true)}</g>`;
// something small that drifts off and fades: exhaust, bubbles, notes
const drift = (dx, dy, dur, delay, inner) => `<g opacity="0">${inner}<animateTransform attributeName="transform" type="translate" values="0 0;${dx} ${dy}" dur="${dur}s" begin="${delay}s" repeatCount="indefinite"/>` +
  `<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.6;1" dur="${dur}s" begin="${delay}s" repeatCount="indefinite"/></g>`;
const note = (x, y, dx, dy, dur, delay) => drift(dx, dy, dur, delay, `<ellipse cx="${x}" cy="${y}" rx="2.1" ry="1.6" fill="K" stroke="none" transform="rotate(-20 ${x} ${y})"/><path d="M${x + 1.9} ${y - .4}V${y - 8}L${x + 5.5} ${y - 6.5}"/>`);
const wheelK = (cx, cy, r, dur = .8, more = false) => `<circle cx="${cx}" cy="${cy}" r="${r}"/>` +
  spin(cx, cy, dur, `<path stroke-width="1.3" d="M${cx - r} ${cy}H${cx + r}M${cx} ${cy - r}V${cy + r}${more ? `M${cx - r * .7} ${cy - r * .7}L${cx + r * .7} ${cy + r * .7}M${cx - r * .7} ${cy + r * .7}L${cx + r * .7} ${cy - r * .7}` : ""}"/>`) +
  `<circle cx="${cx}" cy="${cy}" r="1.3" fill="K"/>`;
const road = (y = 56, dur = .5) => `<path stroke-width="1.6" d="M-12 ${y}H76" stroke-dasharray="7 6"><animate attributeName="stroke-dashoffset" values="0;13" dur="${dur}s" repeatCount="indefinite"/></path>`;

const ART = {
  // ---------------- vehicles
  motorcycle: {
    c: `<circle cx="14" cy="45" r="8" fill="B"/><circle cx="50" cy="45" r="8" fill="B"/>` + bob(0, -.8, .35, `<path d="M19 33L27 26H43L47 34L39 43H26Z"/>`),
    k: wheelK(14, 45, 8, .7) + wheelK(50, 45, 8, .7) + road() +
      bob(0, -.8, .35, `<path d="M14 45L25 35H41M39 43L46 30M50 45L45 24M40 22L49 25"/><path d="M26 34Q33 24 44 30L41 36Z"/><path d="M17 31Q23 28 28 33"/><circle cx="48" cy="30" r="2.3" fill="P"/><path d="M33 42H13"/>`) +
      drift(-9, -3, .9, 0, `<circle cx="9" cy="42" r="1.6"/>`) + drift(-9, -5, .9, .45, `<circle cx="9" cy="42" r="2.2"/>`)
  },
  car: {
    c: bob(0, -.7, .4, `<path d="M6 46V38Q6 34 12 33L20 31L27 21H43L50 31L56 33Q60 34 60 39V46Z"/><path d="M29 25L24 31H35V25ZM38 25V31H47L42 25Z" fill="P"/><path d="M29 25L24 31H35V25ZM38 25V31H47L42 25Z" fill="B"/>`) + `<circle cx="19" cy="47" r="6" fill="P"/><circle cx="47" cy="47" r="6" fill="P"/>`,
    k: road() + bob(0, -.7, .4, `<path d="M6 46V38Q6 34 12 33L20 31L27 21H43L50 31L56 33Q60 34 60 39V46Z"/><path d="M29 25L24 31H35V25ZM38 25V31H47L42 25Z"/><path d="M36 35H40"/><path d="M57 38H60"/>`) +
      `<circle cx="19" cy="47" r="6" fill="P"/><circle cx="47" cy="47" r="6" fill="P"/>` + wheelK(19, 47, 6, .6) + wheelK(47, 47, 6, .6) +
      drift(-8, -2, 1, 0, `<circle cx="3" cy="44" r="1.6"/>`)
  },
  bus: {
    c: bob(0, -.6, .45, `<path d="M6 46V20Q6 15 11 15H53Q58 15 58 20V46Z"/><path d="M10 20H21V30H10ZM24 20H35V30H24ZM38 20H49V30H38Z" fill="P"/><path d="M10 20H21V30H10ZM24 20H35V30H24ZM38 20H49V30H38Z" fill="B"/>`) + `<circle cx="18" cy="47" r="5.5" fill="P"/><circle cx="46" cy="47" r="5.5" fill="P"/>`,
    k: road() + bob(0, -.6, .45, `<path d="M6 46V20Q6 15 11 15H53Q58 15 58 20V46Z"/><path d="M10 20H21V30H10ZM24 20H35V30H24ZM38 20H49V30H38Z"/><path d="M6 36H58"/><path d="M52 20V30H58"/><path d="M55 40H58"/>`) +
      `<circle cx="18" cy="47" r="5.5" fill="P"/><circle cx="46" cy="47" r="5.5" fill="P"/>` + wheelK(18, 47, 5.5, .6) + wheelK(46, 47, 5.5, .6)
  },
  bicycle: {
    c: `<circle cx="15" cy="43" r="10" fill="B"/><circle cx="49" cy="43" r="10" fill="B"/><path d="M27 28H43L33 43Z"/>`,
    k: wheelK(15, 43, 10, 1.1, true) + wheelK(49, 43, 10, 1.1, true) + road(57, .7) +
      `<path d="M15 43L27 28H43L49 43M27 28L33 43H15M33 43L43 28"/><path d="M23 24H31M27 28V24"/><path d="M43 28L41 19H48"/>` +
      spin(33, 43, .9, `<path d="M29 39L37 47M27 39H31M35 47H39"/>`)
  },
  sailboat: {
    c: sway(32, 52, 5, 2.4, `<path d="M10 44H54L47 54H17Z"/><path d="M34 12L52 40H34Z" fill="B"/><path d="M30 18L16 40H30Z"/>`),
    k: sway(32, 52, 5, 2.4, `<path d="M10 44H54L47 54H17Z"/><path d="M32 44V8"/><path d="M34 12L52 40H34Z"/><path d="M30 18L16 40H30Z"/><path d="M32 8L39 10L32 12" fill="K"/>`) +
      `<g><path stroke-width="1.6" d="M-18 58q4 -4 8 0t8 0t8 0t8 0t8 0t8 0t8 0t8 0t8 0t8 0t8 0t8 0"/>${at("translate", "0 0;-16 0", 1.3)}</g>`
  },
  // ---------------- animals
  bird: {
    c: bob(0, -2.5, .7, `<path d="M12 37Q22 25 38 31Q45 23 54 30L48 35Q46 45 30 45Q18 45 12 37Z"/><path d="M53 29L61 32L52 34Z" fill="B"/>` + sway(28, 35, 24, .35, `<path d="M22 34Q30 12 42 16Q40 30 34 36Z" fill="B"/>`)),
    k: bob(0, -2.5, .7, `<path d="M12 37Q22 25 38 31Q45 23 54 30L48 35Q46 45 30 45Q18 45 12 37Z"/><path d="M53 29L61 32L52 34"/><circle cx="48" cy="30" r="1.4" fill="K"/><path d="M13 37L4 33M13 39L4 42"/>` +
      sway(28, 35, 24, .35, `<path d="M22 34Q30 12 42 16Q40 30 34 36"/>`)) +
      `<path stroke-width="1.4" d="M2 14H12M0 22H7M52 52H62"/>`
  },
  fish: {
    c: bob(1.5, -1.5, 1.3, `<path d="M14 32Q28 15 46 27Q53 32 46 38Q28 49 14 32Z"/><path d="M27 23Q31 15 38 21Z" fill="B"/>` + sway(15, 32, 16, .5, `<path d="M15 32L3 23V41Z" fill="B"/>`)),
    k: bob(1.5, -1.5, 1.3, `<path d="M14 32Q28 15 46 27Q53 32 46 38Q28 49 14 32Z"/><path d="M27 23Q31 15 38 21"/><circle cx="42" cy="29" r="1.5" fill="K"/><path d="M36 25Q33 32 36 39"/><path d="M24 31H29M25 35H29"/>` +
      sway(15, 32, 16, .5, `<path d="M15 32L3 23V41Z"/>`)) +
      drift(1, -16, 1.8, 0, `<circle cx="55" cy="27" r="1.8"/>`) + drift(-2, -18, 1.8, .9, `<circle cx="58" cy="30" r="1.2"/>`)
  },
  cat: {
    c: sway(44, 53, 12, 1.2, `<path d="M43 54Q60 52 55 34L51 35Q54 48 43 49Z" fill="B"/>`) + `<path d="M21 56Q17 36 29 31H39Q49 36 45 56Z"/><path d="M24 22Q24 12 25 5L32 11H36L43 5Q44 12 44 22Q44 31 34 31Q24 31 24 22Z"/>`,
    k: sway(44, 53, 12, 1.2, `<path d="M43 54Q60 52 55 34L51 35Q54 48 43 49"/>`) + `<path d="M21 56Q17 36 29 31M39 31Q49 36 45 56Z"/><path d="M21 56H45"/><path d="M24 22Q24 12 25 5L32 11H36L43 5Q44 12 44 22Q44 31 34 31Q24 31 24 22Z"/>` +
      `<ellipse cx="30" cy="20" rx="1.5" ry="2.2" fill="K" stroke="none"><animate attributeName="ry" values="2.2;2.2;.2;2.2;2.2" keyTimes="0;.46;.5;.54;1" dur="3s" repeatCount="indefinite"/></ellipse>` +
      `<ellipse cx="38" cy="20" rx="1.5" ry="2.2" fill="K" stroke="none"><animate attributeName="ry" values="2.2;2.2;.2;2.2;2.2" keyTimes="0;.46;.5;.54;1" dur="3s" repeatCount="indefinite"/></ellipse>` +
      `<path d="M33 24.5H35L34 26Z" fill="K"/><path stroke-width="1.2" d="M27 25L19 23M27 27L19 28M41 25L49 23M41 27L49 28"/><path d="M29 56V48M39 56V48"/>`
  },
  snail: {
    c: bob(2, 0, 1.6, `<path d="M6 52H50Q60 52 60 42V33Q60 29 56.5 29Q53 29 53 33V39Q53 44 48 44H16Q6 44 6 52Z"/><circle cx="31" cy="32" r="14" fill="B"/>`),
    k: bob(2, 0, 1.6, `<path d="M6 52H50Q60 52 60 42V33Q60 29 56.5 29Q53 29 53 33V39Q53 44 48 44M17 44Q6 44 6 52Z"/><circle cx="31" cy="32" r="14" fill="none"/><path d="M32 33Q36 32 36 36Q35 41 29 40Q22 38 23 31Q25 23 34 24Q43 26 43 35"/>` +
      sway(56, 30, 9, .8, `<path d="M55 30L52 20M58 30L61 20"/><circle cx="52" cy="19" r="1.3" fill="K"/><circle cx="61" cy="19" r="1.3" fill="K"/>`)) +
      `<path stroke-width="1.6" d="M-6 56H70" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" values="0;8" dur="1.6s" repeatCount="indefinite"/></path>`
  },
  rabbit: {
    c: bob(0, -7, .8, `<path d="M16 43Q16 32 30 32Q44 32 44 43Q44 54 30 54Q16 54 16 43Z"/><circle cx="45" cy="29" r="8"/>` + sway(45, 24, 7, .8, `<path d="M41 24Q36 6 42 6Q47 8 46 23ZM47 22Q49 7 53 9Q56 13 50 25Z" fill="B"/>`)),
    k: `<path stroke-width="1.6" d="M14 58H50"/>` + bob(0, -7, .8, sway(45, 24, 7, .8, `<path d="M41 24Q36 6 42 6Q47 8 46 23M47 22Q49 7 53 9Q56 13 50 25"/>`) +
      `<path d="M16 43Q16 32 30 32Q44 32 44 43Q44 54 30 54Q16 54 16 43Z"/><circle cx="45" cy="29" r="8" fill="A"/><circle cx="48" cy="28" r="1.4" fill="K"/><path d="M52.5 31.5L53.5 32.5"/>` +
      `<circle cx="15" cy="42" r="4" fill="P"/><path d="M26 54H40M22 46Q26 42 31 45"/>`)
  },
  // ---------------- plants
  tree: {
    c: `<path d="M28 57V36H36V57Z" fill="B"/>` + sway(32, 44, 3.5, 2.2, `<path d="M18 38Q9 36 11 27Q11 19 20 18Q22 7 33 8Q44 8 46 19Q55 20 54 30Q53 38 44 38Z"/>`),
    k: `<path d="M28 57V37M36 37V57M18 57H46"/><path stroke-width="1.4" d="M32 50V43M32 46L35 43"/>` + sway(32, 44, 3.5, 2.2, `<path d="M18 38Q9 36 11 27Q11 19 20 18Q22 7 33 8Q44 8 46 19Q55 20 54 30Q53 38 44 38Z"/><path stroke-width="1.4" d="M22 27Q26 24 29 28M36 20Q40 18 43 22"/>`) +
      drift(-8, 20, 2.4, 0, `<path d="M50 34Q54 32 55 36Q51 38 50 34Z" fill="K"/>`)
  },
  flower: {
    c: sway(32, 58, 7, 1.8, `<path d="M31 49Q20 48 19 39Q29 39 31 49ZM33 45Q43 43 45 34Q35 35 33 45Z" fill="B"/><circle cx="32" cy="12" r="5.5"/><circle cx="41" cy="17" r="5.5"/><circle cx="41" cy="27" r="5.5"/><circle cx="32" cy="32" r="5.5"/><circle cx="23" cy="27" r="5.5"/><circle cx="23" cy="17" r="5.5"/><circle cx="32" cy="22" r="5" fill="P"/><circle cx="32" cy="22" r="5" fill="B"/>`),
    k: `<path stroke-width="1.6" d="M20 58H44"/>` + sway(32, 58, 7, 1.8, `<path d="M32 58Q30 46 32 37"/><path d="M31 49Q20 48 19 39Q29 39 31 49ZM33 45Q43 43 45 34Q35 35 33 45Z"/>` +
      `<circle cx="32" cy="12" r="5.5"/><circle cx="41" cy="17" r="5.5"/><circle cx="41" cy="27" r="5.5"/><circle cx="32" cy="32" r="5.5"/><circle cx="23" cy="27" r="5.5"/><circle cx="23" cy="17" r="5.5"/><circle cx="32" cy="22" r="5" fill="P"/><circle cx="32" cy="22" r="1.2" fill="K"/>`)
  },
  cactus: {
    c: sway(32, 58, 2.5, 1.6, `<path d="M25 58V20Q25 12 32 12Q39 12 39 20V58Z"/><path d="M25 44H19Q12 44 12 37V30Q12 26 15.5 26Q19 26 19 30V37H25ZM39 48H45Q52 48 52 41V33Q52 29 48.5 29Q45 29 45 33V41H39Z"/><circle cx="32" cy="10" r="3.4" fill="B"><animate attributeName="r" values="2.6;4;2.6" dur="1.4s" repeatCount="indefinite"/></circle>`),
    k: `<path stroke-width="1.6" d="M8 58H56"/>` + sway(32, 58, 2.5, 1.6, `<path d="M25 58V20Q25 12 32 12Q39 12 39 20V58"/><path d="M25 44H19Q12 44 12 37V30Q12 26 15.5 26Q19 26 19 30V37H25M39 48H45Q52 48 52 41V33Q52 29 48.5 29Q45 29 45 33V41H39"/>` +
      `<path stroke-width="1.3" d="M32 20V24M29 30H26M35 30H38M32 36V40M29 48H26M35 52H38M15 32H13M49 36H51"/><circle cx="32" cy="10" r="3.4"><animate attributeName="r" values="2.6;4;2.6" dur="1.4s" repeatCount="indefinite"/></circle>`)
  },
  sprout: {
    c: `<path d="M21 42H43L40 58H24Z" fill="B"/><path d="M19 37H45V42H19Z" fill="B"/>` + sway(32, 30, 9, 1.5, `<path d="M32 30Q18 28 15 13Q30 13 32 30Z"/>`) + sway(32, 30, -9, 1.5, `<path d="M32 30Q46 28 49 13Q34 13 32 30Z"/>`),
    k: `<path d="M21 42H43L40 58H24Z"/><path d="M19 37H45V42H19Z"/><path d="M32 37V29"/>` + sway(32, 30, 9, 1.5, `<path d="M32 30Q18 28 15 13Q30 13 32 30Z"/><path stroke-width="1.3" d="M30 27L20 17"/>`) + sway(32, 30, -9, 1.5, `<path d="M32 30Q46 28 49 13Q34 13 32 30Z"/><path stroke-width="1.3" d="M34 27L44 17"/>`)
  },
  // ---------------- instruments
  guitar: {
    c: sway(32, 40, 5, 1.2, `<g transform="rotate(32 32 34)"><path d="M32 30Q23 30 23 37Q23 41 26 43Q20 46 20 53Q20 61 32 61Q44 61 44 53Q44 46 38 43Q41 41 41 37Q41 30 32 30Z"/><path d="M30 30V8H34V30Z" fill="B"/><circle cx="32" cy="41" r="3.6" fill="P"/></g>`),
    k: sway(32, 40, 5, 1.2, `<g transform="rotate(32 32 34)"><path d="M32 30Q23 30 23 37Q23 41 26 43Q20 46 20 53Q20 61 32 61Q44 61 44 53Q44 46 38 43Q41 41 41 37Q41 30 32 30Z"/><path d="M30 30V8H34V30"/><path d="M28.5 2H35.5V8H28.5Z" fill="K"/><circle cx="32" cy="41" r="3.6" fill="P"/><path d="M27 53H37"/><path stroke-width="1" d="M31 8V53M33 8V53"/></g>`) +
      note(14, 22, -3, -12, 1.6, 0) + note(8, 36, -4, -12, 1.6, .8)
  },
  drum: {
    c: `<path d="M12 34V48Q12 56 32 56Q52 56 52 48V34Z"/><ellipse cx="32" cy="34" rx="20" ry="6.5" fill="P"/><ellipse cx="32" cy="34" rx="20" ry="6.5" fill="B"/>`,
    k: `<path d="M12 34V48Q12 56 32 56Q52 56 52 48V34"/><ellipse cx="32" cy="34" rx="20" ry="6.5"/><path stroke-width="1.4" d="M12 41L22 54L32 43L42 54L52 41"/>` +
      sway(22, 32, 13, .3, `<path stroke-width="2.6" d="M24 33L9 13"/><circle cx="9" cy="13" r="1.6" fill="K"/>`) + sway(42, 32, -13, .3, `<path stroke-width="2.6" d="M40 33L55 13"/><circle cx="55" cy="13" r="1.6" fill="K"/>`) +
      note(30, 22, 2, -13, 1.4, 0)
  },
  trumpet: {
    c: bob(0, -1.2, .5, `<path d="M42 27Q53 25 60 15V47Q53 37 42 35Z"/><path d="M8 28H42V34H8Z"/><path d="M19 17H23V28H19ZM26 17H30V28H26ZM33 17H37V28H33Z" fill="B"/>`),
    k: bob(0, -1.2, .5, `<path d="M42 27Q53 25 60 15V47Q53 37 42 35"/><path d="M8 28H42M8 34H42M8 25V37"/><path d="M15 34Q15 44 24 44H32Q40 44 40 34"/>` +
      bob(0, 2.5, .4, `<path d="M19 17H23V28H19Z"/>`) + bob(0, 2.5, .6, `<path d="M26 17H30V28H26Z"/>`) + bob(0, 2.5, .5, `<path d="M33 17H37V28H33Z"/>`)) +
      note(50, 12, 3, -10, 1.3, 0) + note(40, 16, -2, -11, 1.3, .65)
  },
  keyboard: {
    c: `<path d="M5 30Q5 26 9 26H55Q59 26 59 30V50Q59 54 55 54H9Q5 54 5 50Z"/><path d="M9 37H55V51H9Z" fill="P"/>` +
      `<path d="M15.6 37H22.2V51H15.6Z" fill="B"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.3;.35;1" dur="1.2s" repeatCount="indefinite"/></path>` +
      `<path d="M35.4 37H42V51H35.4Z" fill="B"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.4;.45;.7;.75;1" dur="1.2s" repeatCount="indefinite"/></path>`,
    k: `<path d="M5 30Q5 26 9 26H55Q59 26 59 30V50Q59 54 55 54H9Q5 54 5 50Z"/><path d="M9 37H55V51H9Z"/><path stroke-width="1.3" d="M15.6 37V51M22.2 37V51M28.8 37V51M35.4 37V51M42 37V51M48.6 37V51"/>` +
      `<path stroke="none" fill="K" d="M13.8 37H17.4V45H13.8ZM20.4 37H24V45H20.4ZM33.6 37H37.2V45H33.6ZM40.2 37H43.8V45H40.2ZM46.8 37H50.4V45H46.8Z"/><circle cx="12" cy="31.5" r="1.6"/><circle cx="18" cy="31.5" r="1.6"/><path d="M40 31.5H54"/>` +
      note(22, 20, 3, -11, 1.5, 0) + note(40, 22, -2, -12, 1.5, .75)
  }
};

export const CATEGORIES = {
  animal: ["bird", "fish", "cat", "snail", "rabbit"],
  vehicle: ["motorcycle", "car", "bus", "bicycle", "sailboat"],
  plant: ["tree", "flower", "cactus", "sprout"],
  instrument: ["guitar", "drum", "trumpet", "keyboard"]
};
const INKS = [["#F2369B", "#2F6FE4"], ["#2F6FE4", "#F2369B"], ["#F2369B", "#FFC61A"], ["#2F6FE4", "#FFC61A"], ["#FF6C2F", "#2F6FE4"], ["#00A19A", "#F2369B"], ["#00A19A", "#FFC61A"], ["#FF6C2F", "#00A19A"]];
const PAPERS = ["#F8F6EA", "#F4EFDF", "#F1F0EA", "#FBF4E4"];

const rnd = () => crypto.getRandomValues(new Uint32Array(1))[0] / 4294967296;
const pick = a => a[Math.floor(rnd() * a.length)];
const between = (a, b) => a + rnd() * (b - a);
const shuffled = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
// every drawing comes out a little different: its points nudged, its timing stretched, tilted, mirrored, re-inked
const nudge = s => s.replace(/\b(d|cx|cy)="([^"]*)"/g, (m, k, v) => `${k}="${v.replace(/-?\d+(\.\d+)?/g, n => (parseFloat(n) + (rnd() - .5) * .5).toFixed(2))}"`);

export function tile(kind) {
  const D = ART[kind], [A, B] = pick(INKS), paper = pick(PAPERS), id = "h" + Math.floor(rnd() * 0xffffff).toString(16), pace = between(.85, 1.25);
  const ink = s => nudge(s).replace(/fill="([ABPK])"/g, (m, c) => `fill="${c === "A" ? A : c === "B" ? B : c === "P" ? paper : K}"`).replace(/dur="([\d.]+)s"/g, (m, d) => `dur="${(d * pace).toFixed(2)}s"`);
  const sc = between(.8, .9), flip = rnd() < .5 ? -1 : 1, ang = between(0, Math.PI * 2), off = between(1.1, 1.9);
  const fig = `translate(${between(30, 34).toFixed(1)} ${between(31, 34).toFixed(1)}) rotate(${between(-5, 5).toFixed(1)}) scale(${(flip * sc).toFixed(2)} ${sc.toFixed(2)}) translate(-32 -32)`;
  const back = rnd() < .6
    ? `<circle cx="${between(22, 42).toFixed(0)}" cy="${between(22, 38).toFixed(0)}" r="${between(18, 24).toFixed(0)}" fill="url(#${id})"/>`
    : `<path d="M-4 ${between(30, 44).toFixed(0)}H68V${between(8, 20).toFixed(0)}H-4Z" fill="url(#${id})" transform="rotate(${between(-12, 12).toFixed(0)} 32 32)"/>`;
  const grain = Array.from({ length: 7 }, () => `<circle cx="${between(0, 64).toFixed(0)}" cy="${between(0, 64).toFixed(0)}" r="${between(.3, .9).toFixed(1)}" fill="${K}" opacity=".12"/>`).join("");
  return `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><pattern id="${id}" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(${between(15, 75).toFixed(0)})"><circle cx="1.6" cy="1.6" r=".95" fill="${B}"/></pattern></defs>` +
    `<rect width="64" height="64" fill="${paper}"/><g opacity=".5">${back}</g>${grain}<g transform="${fig}">` +
    `<g transform="translate(${(Math.cos(ang) * off).toFixed(2)} ${(Math.sin(ang) * off).toFixed(2)})" fill="${A}" stroke="none" style="mix-blend-mode:multiply">${ink(D.c)}</g>` +
    `<g fill="none" stroke="${K}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">${ink(D.k)}</g></g></svg>`;
}

// Nine squares: one kind of thing to shoot (three or four of it) among others that are not it.
export function squares() {
  const ask = pick(Object.keys(CATEGORIES)), n = 3 + (rnd() < .5 ? 1 : 0), spots = shuffled([0, 1, 2, 3, 4, 5, 6, 7, 8]);
  const yes = shuffled(CATEGORIES[ask]), no = shuffled(Object.keys(CATEGORIES).filter(c => c !== ask).flatMap(c => CATEGORIES[c]));
  const tiles = Array(9); let mask = 0;
  spots.forEach((at9, i) => { if (i < n) mask |= 1 << at9; tiles[at9] = tile(i < n ? yes[i % yes.length] : no[(i - n) % no.length]); });
  return { ask, tiles, mask };
}
export const KINDS = Object.keys(ART);
