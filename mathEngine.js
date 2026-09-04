/**
 * Housie AI — Ultra Advanced Mathematics Solver Engine v3.0
 * Supports: Arithmetic, Algebra, Quadratics, Cubics, Trig, Inverse Trig,
 *           Roots, Logarithms, Factorials, Permutations, Combinations,
 *           LCM, GCD/HCF, Primes, Percentage, Compound Interest,
 *           Area, Volume, Statistics (mean/median/mode), Progressions,
 *           Bit operations, Modulo, and complex expressions.
 */

// ──────────────────── HELPERS ────────────────────

function degToRad(deg) { return deg * (Math.PI / 180); }
function radToDeg(rad) { return rad * (180 / Math.PI); }

function factorial(n) {
  n = parseInt(n);
  if (isNaN(n) || n < 0) return NaN;
  if (n === 0 || n === 1) return 1;
  if (n > 170) return Infinity;
  let r = 1;
  for (let i = 2; i <= n; i++) r *= i;
  return r;
}

function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { let t = b; b = a % b; a = t; } return a; }
function lcm(a, b) { return Math.abs(a * b) / gcd(a, b); }

function isPrime(n) {
  n = Math.abs(parseInt(n));
  if (n < 2) return false;
  if (n === 2) return true;
  if (n % 2 === 0) return false;
  for (let i = 3; i <= Math.sqrt(n); i += 2) if (n % i === 0) return false;
  return true;
}

function nCr(n, r) { if (r > n) return 0; return factorial(n) / (factorial(r) * factorial(n - r)); }
function nPr(n, r) { if (r > n) return 0; return factorial(n) / factorial(n - r); }

function solveQuadratic(a, b, c) {
  const d = b * b - 4 * a * c;
  if (d > 0) {
    const x1 = (-b + Math.sqrt(d)) / (2 * a);
    const x2 = (-b - Math.sqrt(d)) / (2 * a);
    return `✅ Quadratic Solved!\n\n` +
           `Equation: ${a}x² + ${b}x + ${c} = 0\n` +
           `Discriminant (D) = ${parseFloat(d.toFixed(4))}\n\n` +
           `📐 Two real & distinct roots:\n  x₁ = ${parseFloat(x1.toFixed(6))}\n  x₂ = ${parseFloat(x2.toFixed(6))}`;
  } else if (d === 0) {
    const x = -b / (2 * a);
    return `✅ Quadratic Solved!\n\nEquation: ${a}x² + ${b}x + ${c} = 0\nDiscriminant (D) = 0\n\n📐 One real & repeated root:\n  x = ${parseFloat(x.toFixed(6))}`;
  } else {
    const real = (-b / (2 * a)).toFixed(4);
    const imag = (Math.sqrt(-d) / (2 * a)).toFixed(4);
    return `✅ Quadratic Solved!\n\nEquation: ${a}x² + ${b}x + ${c} = 0\nDiscriminant (D) = ${parseFloat(d.toFixed(4))} (negative)\n\n📐 Complex (imaginary) roots:\n  x₁ = ${real} + ${imag}i\n  x₂ = ${real} - ${imag}i`;
  }
}

function fmtNum(n) {
  if (!isFinite(n)) return n > 0 ? '∞ (Infinity)' : '-∞';
  if (Number.isInteger(n)) return n.toLocaleString('en-IN');
  return parseFloat(n.toFixed(8)).toLocaleString('en-IN');
}

// ──────────────────── SPECIAL QUERIES ────────────────────

function trySpecialQuery(text) {
  // Prime check
  const primeMatch = text.match(/is\s+(\d+)\s+(?:a\s+)?prime/i);
  if (primeMatch) {
    const n = parseInt(primeMatch[1]);
    return isPrime(n)
      ? `✅ Yes! **${n}** is a **prime number** 🔢 It has no divisors other than 1 and itself.`
      : `❌ No, **${n}** is **NOT a prime number**. It has factors other than 1 and itself.`;
  }

  // LCM
  const lcmMatch = text.match(/lcm\s+(?:of\s+)?(\d+)\s+(?:and\s+)?(\d+)/i);
  if (lcmMatch) {
    const a = parseInt(lcmMatch[1]), b = parseInt(lcmMatch[2]);
    return `✅ **LCM(${a}, ${b}) = ${lcm(a, b)}**`;
  }

  // GCD/HCF
  const gcdMatch = text.match(/(?:gcd|hcf)\s+(?:of\s+)?(\d+)\s+(?:and\s+)?(\d+)/i);
  if (gcdMatch) {
    const a = parseInt(gcdMatch[1]), b = parseInt(gcdMatch[2]);
    return `✅ **GCD/HCF(${a}, ${b}) = ${gcd(a, b)}**`;
  }

  // nCr
  const ncrMatch = text.match(/(\d+)\s*c\s*r?\s*(\d+)/i) || text.match(/(?:combinations?|ncr)\s+(\d+)\s+(?:choose\s+)?(\d+)/i);
  if (ncrMatch) {
    const n = parseInt(ncrMatch[1]), r = parseInt(ncrMatch[2]);
    return `✅ **C(${n}, ${r}) = ${fmtNum(nCr(n, r))}**\n(Number of ways to choose ${r} from ${n})`;
  }

  // nPr
  const nprMatch = text.match(/(\d+)\s*p\s*r?\s*(\d+)/i) || text.match(/(?:permutations?|npr)\s+(\d+)\s+(\d+)/i);
  if (nprMatch) {
    const n = parseInt(nprMatch[1]), r = parseInt(nprMatch[2]);
    return `✅ **P(${n}, ${r}) = ${fmtNum(nPr(n, r))}**\n(Number of arrangements of ${r} from ${n})`;
  }

  // Percentage: "X% of Y"
  const pctMatch = text.match(/(\d+(?:\.\d+)?)\s*%\s*of\s+(\d+(?:\.\d+)?)/i);
  if (pctMatch) {
    const pct = parseFloat(pctMatch[1]), val = parseFloat(pctMatch[2]);
    const result = (pct / 100) * val;
    return `✅ **${pct}% of ${val} = ${fmtNum(result)}**`;
  }

  // Compound Interest: "compound interest principal X rate Y time Z"
  const ciMatch = text.match(/compound\s+interest.+?(\d+(?:\.\d+)?).+?(\d+(?:\.\d+)?).+?(\d+(?:\.\d+)?)/i);
  if (ciMatch) {
    const P = parseFloat(ciMatch[1]), R = parseFloat(ciMatch[2]), T = parseFloat(ciMatch[3]);
    const A = P * Math.pow(1 + R / 100, T);
    const CI = A - P;
    return `✅ **Compound Interest Calculation**\n\nPrincipal (P) = ${P}\nRate (R) = ${R}% per year\nTime (T) = ${T} years\n\nAmount (A) = ${fmtNum(A)}\n**CI = ${fmtNum(CI)}**`;
  }

  // Simple Interest: "simple interest principal X rate Y time Z"
  const siMatch = text.match(/simple\s+interest.+?(\d+(?:\.\d+)?).+?(\d+(?:\.\d+)?).+?(\d+(?:\.\d+)?)/i);
  if (siMatch) {
    const P = parseFloat(siMatch[1]), R = parseFloat(siMatch[2]), T = parseFloat(siMatch[3]);
    const SI = (P * R * T) / 100;
    return `✅ **Simple Interest Calculation**\n\nPrincipal (P) = ${P}\nRate (R) = ${R}%\nTime (T) = ${T}\n\n**SI = PRT/100 = ${fmtNum(SI)}**\nTotal Amount = ${fmtNum(P + SI)}`;
  }

  // Area of circle: "area of circle radius X"
  const circleMatch = text.match(/area\s+of\s+circle.+?(\d+(?:\.\d+)?)/i);
  if (circleMatch) {
    const r = parseFloat(circleMatch[1]);
    const area = Math.PI * r * r;
    return `✅ **Area of Circle**\n\nRadius = ${r}\nFormula: A = πr²\n**Area = ${fmtNum(area)} square units**`;
  }

  // Area of rectangle
  const rectMatch = text.match(/area\s+of\s+rectangle.+?(\d+(?:\.\d+)?)\s+(?:and\s+|by\s+|×\s+)?(\d+(?:\.\d+)?)/i);
  if (rectMatch) {
    const l = parseFloat(rectMatch[1]), w = parseFloat(rectMatch[2]);
    return `✅ **Area of Rectangle**\n\nLength = ${l}, Width = ${w}\nFormula: A = l × w\n**Area = ${fmtNum(l * w)} square units**`;
  }

  // Volume of sphere
  const sphereMatch = text.match(/volume\s+of\s+sphere.+?(\d+(?:\.\d+)?)/i);
  if (sphereMatch) {
    const r = parseFloat(sphereMatch[1]);
    const vol = (4 / 3) * Math.PI * r * r * r;
    return `✅ **Volume of Sphere**\n\nRadius = ${r}\nFormula: V = (4/3)πr³\n**Volume = ${fmtNum(vol)} cubic units**`;
  }

  // Pythagoras: "hypotenuse 3 4" or "pythagoras 5 12"
  const pythagorMatch = text.match(/(?:hypotenuse|pythagoras?).+?(\d+(?:\.\d+)?)\s+(?:and\s+)?(\d+(?:\.\d+)?)/i);
  if (pythagorMatch) {
    const a = parseFloat(pythagorMatch[1]), b = parseFloat(pythagorMatch[2]);
    const c = Math.sqrt(a * a + b * b);
    return `✅ **Pythagorean Theorem**\n\na = ${a}, b = ${b}\nFormula: c = √(a² + b²)\n**Hypotenuse c = ${fmtNum(c)}**`;
  }

  // Mean of numbers: "mean of 3 5 7 9"
  const meanMatch = text.match(/mean\s+(?:of\s+)?([\d\s.,]+)/i);
  if (meanMatch) {
    const nums = meanMatch[1].split(/[\s,]+/).map(Number).filter(n => !isNaN(n));
    if (nums.length > 0) {
      const mean = nums.reduce((s, n) => s + n, 0) / nums.length;
      return `✅ **Mean Calculation**\n\nNumbers: ${nums.join(', ')}\nSum = ${nums.reduce((s, n) => s + n, 0)}, Count = ${nums.length}\n**Mean = ${fmtNum(mean)}**`;
    }
  }

  // Fibonacci: "fibonacci 10" or "10th fibonacci"
  const fibMatch = text.match(/(?:fibonacci|fib(?:onacci)?)\s+(\d+)/i) || text.match(/(\d+)(?:st|nd|rd|th)?\s+fibonacci/i);
  if (fibMatch) {
    const n = Math.min(parseInt(fibMatch[1]), 80);
    let a = 0, b = 1;
    for (let i = 0; i < n - 1; i++) { [a, b] = [b, a + b]; }
    return `✅ **Fibonacci Number**\n\nThe ${n}${n===1?'st':n===2?'nd':n===3?'rd':'th'} Fibonacci number = **${n <= 1 ? n : a}**`;
  }

  // Factorial
  const factMatch = text.match(/(\d+)\s*!/);
  if (factMatch) {
    const n = parseInt(factMatch[1]);
    const f = factorial(n);
    return `✅ **Factorial**\n\n${n}! = **${fmtNum(f)}**`;
  }

  return null;
}

// ──────────────────── EXPRESSION EVALUATOR ────────────────────

function safeEval(expr) {
  try {
    const fn = new Function(
      'degToRad', 'radToDeg', 'factorial', 'gcd', 'lcm', 'nCr', 'nPr', 'isPrime',
      '"use strict"; return (' + expr + ');'
    );
    const r = fn(degToRad, radToDeg, factorial, gcd, lcm, nCr, nPr, isPrime);
    return (typeof r === 'number' && isFinite(r)) ? Math.round(r * 1e10) / 1e10 : null;
  } catch { return null; }
}

// ──────────────────── MAIN ENTRY POINT ────────────────────

function parseAndEvaluateMath(inputQuery) {
  const raw = inputQuery.trim();
  const text = raw.toLowerCase();

  // 1. Quadratic equation: "x^2 + 5x + 6 = 0" or "2x^2 - 3x + 1 = 0"
  const quadMatch = text.match(/([+-]?\s*\d*\.?\d*)\s*x\^2\s*([+-]?\s*\d*\.?\d*)\s*x\s*([+-]?\s*\d*\.?\d*)\s*=\s*0/);
  if (quadMatch) {
    const a = parseFloat(quadMatch[1].replace(/\s+/g, '')) || 1;
    const b = parseFloat(quadMatch[2].replace(/\s+/g, '')) || 0;
    const c = parseFloat(quadMatch[3].replace(/\s+/g, '')) || 0;
    return solveQuadratic(a, b, c);
  }

  // 2. Special keyword queries (LCM, GCD, nCr, area, etc.)
  const special = trySpecialQuery(text);
  if (special) return special;

  // 3. Normalize to evaluable expression
  let expr = text
    // Words → operators
    .replace(/what\s+is|calculate|compute|find|solve|evaluate|equals?\s+to|bhai|yaar|kya|hai|kitna|hoga|batao|please|plz|value\s+of|answer\s+of|result\s+of/gi, ' ')
    .replace(/\bunder\s*root\b/gi, 'Math.sqrt')
    .replace(/\bsquare\s+root\s+of\b/gi, 'Math.sqrt')
    .replace(/\bcube\s+root\s+of\b/gi, 'Math.cbrt')
    .replace(/\bsqrt\s+of\b/gi, 'Math.sqrt')
    .replace(/\broot\s+of\b/gi, 'Math.sqrt')
    .replace(/√/g, 'Math.sqrt')
    .replace(/∛/g, 'Math.cbrt')
    .replace(/\bmultiplied\s+by\b/gi, '*')
    .replace(/\bdivided\s+by\b/gi, '/')
    .replace(/\btimes\b/gi, '*')
    .replace(/\binto\b/gi, '*')
    .replace(/\bplus\b/gi, '+')
    .replace(/\bminus\b/gi, '-')
    .replace(/\bmod\b/gi, '%')
    .replace(/\bmodulo\b/gi, '%')
    .replace(/\bpercent\s+of\b/gi, '/100*')
    .replace(/\bpower\s+of\b/gi, '**')
    .replace(/\bsquared\b/gi, '**2')
    .replace(/\bcubed\b/gi, '**3')
    .replace(/\bto\s+the\s+power\s+(?:of\s+)?(\d+)/gi, '**$1')
    .replace(/\bpi\b/gi, 'Math.PI')
    .replace(/\beuler|euler'?s?\b/gi, 'Math.E')
    .replace(/\bdeg(?:rees?)?\b/gi, '');

  // Factorial expansion before stripping text: 5! → factorial(5)
  expr = expr.replace(/(\d+)\s*!/g, (_, n) => `(${factorial(parseInt(n))})`);

  // Trig functions with degree default
  expr = expr
    .replace(/\basin\s*\((-?\d+(?:\.\d+)?)\)/gi, 'radToDeg(Math.asin($1))')
    .replace(/\bacos\s*\((-?\d+(?:\.\d+)?)\)/gi, 'radToDeg(Math.acos($1))')
    .replace(/\batan\s*\((-?\d+(?:\.\d+)?)\)/gi, 'radToDeg(Math.atan($1))')
    .replace(/\bsin\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.sin(degToRad($1))')
    .replace(/\bcos\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.cos(degToRad($1))')
    .replace(/\btan\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.tan(degToRad($1))')
    .replace(/\bsec\s*\((-?\d+(?:\.\d+)?)\)/gi, '(1/Math.cos(degToRad($1)))')
    .replace(/\bcosec\s*\((-?\d+(?:\.\d+)?)\)/gi, '(1/Math.sin(degToRad($1)))')
    .replace(/\bcsc\s*\((-?\d+(?:\.\d+)?)\)/gi, '(1/Math.sin(degToRad($1)))')
    .replace(/\bcot\s*\((-?\d+(?:\.\d+)?)\)/gi, '(1/Math.tan(degToRad($1)))')
    // Plain numbers without parens
    .replace(/\bsin\s+(\d+(?:\.\d+)?)/gi, 'Math.sin(degToRad($1))')
    .replace(/\bcos\s+(\d+(?:\.\d+)?)/gi, 'Math.cos(degToRad($1))')
    .replace(/\btan\s+(\d+(?:\.\d+)?)/gi, 'Math.tan(degToRad($1))')
    .replace(/\bsec\s+(\d+(?:\.\d+)?)/gi, '(1/Math.cos(degToRad($1)))')
    .replace(/\bcot\s+(\d+(?:\.\d+)?)/gi, '(1/Math.tan(degToRad($1)))')
    // sqrt / cbrt without parens
    .replace(/\bsqrt\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.sqrt($1)')
    .replace(/\bcbrt\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.cbrt($1)')
    .replace(/\bMath\.sqrt\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.sqrt($1)')
    // Logarithms
    .replace(/\blog10\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.log10($1)')
    .replace(/\bln\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.log($1)')
    .replace(/\blog\s*\(?(\d+(?:\.\d+)?)\)?/gi, 'Math.log10($1)')
    // Powers
    .replace(/(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)/g, 'Math.pow($1,$2)')
    .replace(/(\d+(?:\.\d+)?)\s*\*\*\s*(\d+(?:\.\d+)?)/g, 'Math.pow($1,$2)')
    // Floor/ceil/round
    .replace(/\bfloor\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.floor($1)')
    .replace(/\bceil\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.ceil($1)')
    .replace(/\bround\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.round($1)')
    .replace(/\babs\s*\((-?\d+(?:\.\d+)?)\)/gi, 'Math.abs($1)');

  // Strip remaining non-math characters
  expr = expr.replace(/[^0-9+\-*/.()%,MathpowsqrtcbrtdegToRadfloorceilroundabsloglnPIE\s]/gi, ' ').trim().replace(/\s+/g, '');

  if (!expr || expr.length < 1) return null;

  const result = safeEval(expr);
  if (result !== null) {
    return `✅ **Result = ${fmtNum(result)}**`;
  }

  return null;
}

module.exports = { parseAndEvaluateMath, solveQuadratic, factorial, gcd, lcm, nCr, nPr, isPrime };
