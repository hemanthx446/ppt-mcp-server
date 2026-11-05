// NOTE FOR THE AGENT: the pres.addSection({ title: ... }) names and the sectionTitle values in this file
// ("Introduction", "Solution", "Workstreams", "Implementation", "Commercials") are DATA FOR THE SGG DECK ONLY.
// Do not copy them. Derive sections from each deck's own storyline (see UPDATE_v3_PROMPT.md section 2),
// and use none for decks under 8 slides. Likewise, text boxes here use wrap-safe pptxgenjs defaults; when
// porting to python-pptx use tools/pptx_text_helpers.py (python-pptx text boxes default to wrap="none").
const pptxgen = require("pptxgenjs");
const React = require("react");
const RDS = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { applyTheme } = require("./apply_theme.js");

// Lumbini Elite palette (from the Lumbini SAP GRC deck)
const THEME = {
  name: "Lumbini Elite",
  headFontFace: "Inter",
  bodyFontFace: "Inter",
  colors: {
    dk1: "141E2D", lt1: "FFFFFF", dk2: "1F497D", lt2: "EEF3F8",
    accent1: "0070C0", accent2: "F78B15", accent3: "0066B4",
    accent4: "646E78", accent5: "DCE1E6", accent6: "1F497D",
    hlink: "0070C0", folHlink: "646E78",
  },
};
const OUT = "./SGG_ELITIA_BI_Odoo_Proposal_Lumbini.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: "Inter", bodyFontFace: "Inter" };
pres.title = "SGG – Enterprise Business Intelligence & Odoo Enhancement Proposal";
pres.company = "Lumbini Elite Solutions &amp; Services Pvt. Ltd.";
const C = pres.SchemeColor;
const S = pres.shapes;
const HP = S.HOME_PLATE || S.PENTAGON;
const SEMI = "Inter SemiBold";
const BG = "../themes/lumbini/assets/bg_light.jpg";

async function icon(Comp, color = "#FFFFFF") {
  const svg = RDS.renderToStaticMarkup(React.createElement(Comp, { color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const shadow = () => ({ type: "outer", color: "000000", opacity: 0.16, blur: 8, offset: 2, angle: 90 });

const FOOT = "Lumbini Elite Solutions & Services Pvt. Ltd.  |  Confidential proposal for SGG";
function corner(objs) {
  const b = C.accent3;
  [[11.6, 0, 0.24, 0.535], [11.6, 0.293, 1.73, 0.24], [12.24, 0, 0.24, 1.1], [12.24, 0.86, 1.09, 0.24]].forEach((r) =>
    objs.push({ rect: { x: r[0], y: r[1], w: r[2], h: r[3], fill: { color: b } } }));
  objs.push({ rect: { x: 0, y: 6.72, w: 0.3, h: 0.78, fill: { color: b } } });
}
const cobj = [];
corner(cobj);
pres.defineSlideMaster({
  title: "CONTENT",
  background: { path: BG },
  objects: [
    ...cobj,
    { placeholder: { options: { name: "title", type: "title", x: 0.65, y: 0.64, w: 10.7, h: 0.7, fontSize: 24, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: 0.65, y: 7.1, w: 9, h: 0.25, fontSize: 9, color: C.accent4, margin: 0, valign: "middle" } } },
  ],
  slideNumber: { x: 11.2, y: 7.1, w: 0.9, h: 0.25, fontSize: 9, color: C.accent4, align: "right" },
});
pres.defineSlideMaster({
  title: "COVER",
  background: { path: BG },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.9, y: 2.45, w: 9.6, h: 2.0, fontSize: 36, bold: true, color: C.text1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
  ],
});

const txt = (s, t, o = {}) =>
  s.addText(t, { isTextBox: true, margin: 0, color: C.text1, fontSize: 13, valign: "top", ...o });
const eyebrow = (s, t) => txt(s, t.toUpperCase(), { x: 0.65, y: 0.36, w: 8, h: 0.26, fontSize: 11, fontFace: SEMI, color: C.accent1, valign: "middle" });
const subtitle = (s, t) => txt(s, t, { x: 0.65, y: 1.36, w: 10.7, h: 0.35, fontSize: 13, color: C.accent4, valign: "middle" });
function line(s, x1, y1, x2, y2, o = {}) {
  s.addShape(S.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: o.color || C.accent4, width: o.width || 1.5, endArrowType: o.end, beginArrowType: o.begin, dashType: o.dash },
  });
}
function circleNum(s, cx, cy, d, label, fill, fs = 15) {
  s.addShape(S.OVAL, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: fill }, line: { color: fill, width: 0 } });
  txt(s, label, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, align: "center", valign: "middle", fontSize: fs, bold: true, color: C.background1 });
}
function card(s, x, y, w, h, o = {}) {
  s.addShape(S.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: o.r || 0.22, fill: { color: C.background1 }, line: { color: C.accent5, width: 1 }, shadow: shadow() });
}

(async () => {
  const ic = {
    check: await icon(fa.FaCheckCircle, "#0070C0"), info: await icon(fa.FaInfoCircle, "#646E78"),
    clip: await icon(fa.FaClipboardCheck), eye: await icon(fa.FaSearch), table: await icon(fa.FaThList), map: await icon(fa.FaRoute),
  };

  // ================= 1 COVER =================
  pres.addSection({ title: "Introduction" });
  {
    const s = pres.addSlide({ masterName: "COVER", sectionTitle: "Introduction" });
    s.addImage({ path: "../themes/lumbini/assets/illus.png", x: 0.25, y: 0.2, w: 2.8, h: 2.9, transparency: 35 });
    s.addImage({ path: "../themes/lumbini/assets/logo.png", x: 10.35, y: 0.5, w: 2.4, h: 1.017 });
    s.addText("SGG – Enterprise Business Intelligence & Odoo Enhancement Proposal", { placeholder: "title" });
    line(s, 0.9, 4.68, 6.2, 4.68, { color: C.accent2, width: 3 });
    txt(s, "Centralized Insights  |  Improved ERP Experience  |  Connected Business Processes", { x: 0.9, y: 4.85, w: 9.4, h: 0.4, fontSize: 15, fontFace: SEMI, color: C.accent1 });
    const rows = [
      ["Prepared for", "Saeed Godharan Group (SGG)"],
      ["Prepared by", "Lumbini Elite Solutions & Services Pvt. Ltd."],
      ["Proposed solution", "ELITIA BI"],
      ["Proposal date", "2 November 2026"],
    ];
    rows.forEach((r, i) => {
      txt(s, r[0], { x: 0.9, y: 5.55 + i * 0.36, w: 2.1, h: 0.3, fontSize: 12, fontFace: SEMI, color: C.accent4, valign: "middle" });
      txt(s, r[1], { x: 3.0, y: 5.55 + i * 0.36, w: 6.2, h: 0.3, fontSize: 13, valign: "middle" });
    });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 9.9, y: 6.2, w: 3.9, h: 0.85, rectRadius: 0.4, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
    txt(s, "Proposal  |  ELITIA BI", { x: 10.25, y: 6.2, w: 3.2, h: 0.85, fontSize: 18, bold: true, color: C.background1, valign: "middle" });
    s.addNotes("Cover. Proposal date is today's date; update if issued later.");
  }

  // ================= 2 REQUIREMENTS =================
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Introduction" });
    eyebrow(s, "Business requirements");
    s.addText("Understanding SGG's business requirements", { placeholder: "title" });
    subtitle(s, "From today's challenges to the outcomes SGG is seeking");
    const hx = [0.65, 4.75, 9.2];
    ["REQUIREMENT", "TODAY", "DESIRED OUTCOME"].forEach((h, i) => txt(s, h, { x: hx[i], y: 1.9, w: 3.8, h: 0.28, fontSize: 10.5, fontFace: SEMI, color: i === 2 ? C.accent1 : C.accent4, charSpacing: 3 }));
    const rows = [
      ["Centralized Business Intelligence", "Information is spread across functions. Management needs consolidated reporting and drill-down visibility.", "One view of Finance, HR and Supply Chain, with drill-down to detail.", C.accent1],
      ["Odoo ERP Health Check & UI/UX Audit", "Users face usability challenges in the current Odoo implementation.", "An easier Odoo experience, guided by a prioritized improvement roadmap.", C.text2],
      ["Resort ERP to Odoo Data Migration", "Historical data remains in Resort ERP.", "Historical and missing data available in Odoo, reconciled and signed off.", C.accent2],
      ["Payroll & Biometric Attendance Integration", "Attendance and timesheet information is not connected to payroll.", "Attendance flows into payroll, with WPS-ready salary files for bank upload.", C.accent4],
    ];
    rows.forEach((r, i) => {
      const y = 2.25 + i * 1.12;
      line(s, 0.65, y, 12.68, y, { color: C.accent5, width: 1.25 });
      circleNum(s, 0.92, y + 0.56, 0.52, String(i + 1), r[3], 15);
      txt(s, r[0], { x: 1.5, y: y + 0.08, w: 3.0, h: 0.96, fontSize: 14, bold: true, valign: "middle" });
      txt(s, r[1], { x: 4.75, y: y + 0.08, w: 3.55, h: 0.96, fontSize: 12, color: C.accent4, valign: "middle" });
      s.addShape(S.RIGHT_ARROW, { x: 8.5, y: y + 0.38, w: 0.45, h: 0.36, fill: { color: C.accent1, transparency: 25 }, line: { color: C.accent1, width: 0 } });
      txt(s, r[2], { x: 9.2, y: y + 0.08, w: 3.48, h: 0.96, fontSize: 12, fontFace: SEMI, valign: "middle" });
    });
    s.addNotes("Four requirements from SGG, each shown with today's challenge and the desired outcome.");
  }

  // ================= 3 SOLUTION OVERVIEW =================
  pres.addSection({ title: "Solution" });
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Solution" });
    eyebrow(s, "Proposed solution");
    s.addText("Four connected workstreams around Odoo", { placeholder: "title" });
    subtitle(s, "Each workstream strengthens SGG's Odoo environment as the single system of record");
    const ox = 6.67, oy = 4.0;
    line(s, 4.65, 2.95, 5.78, 3.5, { color: C.accent2, width: 2.25, end: "triangle" });
    line(s, 4.65, 5.3, 5.75, 4.6, { color: C.accent4, width: 2.25, end: "triangle" });
    line(s, 7.78, 4.0, 8.65, 4.0, { color: C.accent1, width: 2.25, end: "triangle" });
    line(s, 6.67, 5.5, 6.67, 5.08, { color: C.text2, width: 2.25, end: "triangle", begin: "triangle" });
    txt(s, "Data in", { x: 4.75, y: 2.35, w: 1.2, h: 0.3, fontSize: 11, italic: true, color: C.accent4 });
    txt(s, "Data in", { x: 5.25, y: 5.05, w: 1.2, h: 0.3, fontSize: 11, italic: true, color: C.accent4 });
    txt(s, "Data out", { x: 7.7, y: 3.6, w: 1.0, h: 0.3, fontSize: 11, italic: true, color: C.accent4, align: "center" });
    txt(s, "Improves", { x: 6.85, y: 5.2, w: 1.1, h: 0.3, fontSize: 11, italic: true, color: C.accent4 });
    s.addShape(S.OVAL, { x: ox - 1.05, y: oy - 1.05, w: 2.1, h: 2.1, fill: { color: C.text2 }, line: { color: C.text2, width: 0 }, shadow: shadow() });
    txt(s, [{ text: "SGG Odoo ERP", options: { fontSize: 16, bold: true, breakLine: true } }, { text: "System of record", options: { fontSize: 11 } }],
      { x: ox - 1.05, y: oy - 1.05, w: 2.1, h: 2.1, align: "center", valign: "middle", color: C.background1 });
    const node = (x, y, w, h, letter, col, title, desc) => {
      card(s, x, y, w, h);
      circleNum(s, x + 0.6, y + h / 2, 0.56, letter, col, 17);
      txt(s, [{ text: title, options: { fontSize: 15, bold: true, breakLine: true } }, { text: desc, options: { fontSize: 12, color: C.accent4 } }],
        { x: x + 1.05, y: y + 0.1, w: w - 1.2, h: h - 0.2, valign: "middle" });
    };
    node(0.65, 2.1, 4.0, 1.6, "C", C.accent2, "Data Migration", "Resort ERP history extracted, cleansed, mapped and validated");
    node(0.65, 4.55, 4.0, 1.6, "D", C.accent4, "Payroll Integration", "Biometric attendance, timesheets, payroll and WPS files");
    node(8.68, 3.2, 4.0, 1.6, "A", C.accent1, "ELITIA BI", "Centralized dashboards and executive reporting");
    node(4.7, 5.55, 4.0, 1.35, "B", C.text2, "Odoo Health Check", "Configuration, usability and improvement opportunities");
    s.addNotes("Odoo is the hub. C and D bring data into Odoo, B improves how Odoo is used, A reads from Odoo to provide centralized reporting.");
  }

  // ================= 4 ELITIA BI =================
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Solution" });
    eyebrow(s, "ELITIA BI");
    s.addText("ELITIA BI: centralized business intelligence", { placeholder: "title" });
    subtitle(s, "Odoo stays the source of truth; ELITIA BI turns it into one governed reporting layer");
    const flow = [["Odoo ERP", C.accent4], ["Data Integration", C.accent3], ["ELITIA BI", C.text2], ["Department Dashboards", C.accent1], ["Executive Insights", C.accent2]];
    flow.forEach((f, i) => {
      const x = 0.65 + i * 2.37;
      s.addShape(i === 0 ? HP : S.CHEVRON, { x, y: 1.85, w: 2.5, h: 0.8, fill: { color: f[1] }, line: { color: C.background1, width: 1.5 } });
      txt(s, f[0], { x: x + (i === 0 ? 0.15 : 0.5), y: 1.85, w: i === 0 ? 1.9 : 1.6, h: 0.8, align: "center", valign: "middle", fontSize: 12, bold: true, color: C.background1 });
    });
    const mx = 0.65, my = 2.85, mw = 7.3, mh = 4.05;
    s.addShape(S.RECTANGLE, { x: mx, y: my, w: mw, h: mh, fill: { color: C.background1 }, line: { color: C.accent5, width: 1 }, shadow: shadow() });
    s.addShape(S.RECTANGLE, { x: mx, y: my, w: mw, h: 0.38, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
    txt(s, "ELITIA BI", { x: mx + 0.15, y: my, w: 2, h: 0.38, fontSize: 11, bold: true, color: C.background1, valign: "middle" });
    txt(s, "Illustrative layout, not SGG data", { x: mx + mw - 3.2, y: my, w: 3.05, h: 0.38, fontSize: 10, italic: true, color: C.accent5, align: "right", valign: "middle" });
    const tabs = ["Executive", "Finance", "HR", "Supply Chain", "Business unit"];
    let tx = mx + 0.15;
    tabs.forEach((t, i) => {
      const w = 0.36 + t.length * 0.088;
      if (i === 1) s.addShape(S.ROUNDED_RECTANGLE, { x: tx, y: my + 0.46, w, h: 0.28, rectRadius: 0.08, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 } });
      txt(s, t, { x: tx, y: my + 0.46, w, h: 0.28, fontSize: 10, align: "center", valign: "middle", color: i === 1 ? C.background1 : C.accent4, bold: i === 1 });
      tx += w + 0.06;
    });
    const kpis = [["Revenue vs plan", "102%", "▲ 4% vs last year"], ["Cost vs budget", "97%", "▼ 2% vs last year"], ["Receivable days", "41", "▼ 3 days vs last yr"], ["Attendance", "94%", "▲ 1% vs last year"]];
    kpis.forEach((k, i) => {
      const x = mx + 0.15 + i * 1.78;
      s.addShape(S.RECTANGLE, { x, y: my + 0.84, w: 1.68, h: 0.82, fill: { color: C.background2 }, line: { color: C.background2, width: 0 } });
      txt(s, k[0], { x: x + 0.1, y: my + 0.88, w: 1.55, h: 0.22, fontSize: 9, color: C.accent4 });
      txt(s, k[1], { x: x + 0.1, y: my + 1.08, w: 1.5, h: 0.32, fontSize: 16, bold: true });
      txt(s, k[2], { x: x + 0.1, y: my + 1.42, w: 1.58, h: 0.2, fontSize: 9, color: C.accent1 });
    });
    const cf = { catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 9, valAxisLabelFontSize: 9, catAxisLabelColor: "646E78", valAxisLabelColor: "646E78", valGridLine: { color: "DCE1E6", size: 0.5 }, catGridLine: { style: "none" }, titleFontFace: "+mn-lt", titleFontSize: 10, titleColor: "141E2D", showTitle: true };
    s.addChart(pres.charts.BAR, [{ name: "Revenue vs plan (%)", labels: ["BU A", "BU B", "BU C", "BU D", "BU E"], values: [108, 101, 96, 92, 85] }],
      { x: mx + 0.1, y: my + 1.75, w: 3.5, h: 2.25, barDir: "col", chartColors: ["0070C0"], title: "Revenue vs plan by business unit (%)", showLegend: false, showValue: true, dataLabelFontSize: 9, dataLabelFontFace: "+mn-lt", dataLabelColor: "141E2D", dataLabelPosition: "outEnd", valAxisMinVal: 0, valAxisMaxVal: 130, valAxisHidden: true, ...cf, valGridLine: { style: "none" } });
    s.addChart(pres.charts.LINE, [
      { name: "Actual", labels: ["M1", "M2", "M3", "M4", "M5", "M6"], values: [92, 95, 99, 97, 103, 102] },
      { name: "Plan", labels: ["M1", "M2", "M3", "M4", "M5", "M6"], values: [95, 96, 97, 98, 99, 100] }],
      { x: mx + 3.7, y: my + 1.75, w: 3.5, h: 2.25, chartColors: ["0070C0", "F78B15"], title: "Revenue trend vs plan (%)", showLegend: true, legendPos: "b", legendFontSize: 9, legendFontFace: "+mn-lt", lineSize: 2, lineDataSymbolSize: 5, valAxisMinVal: 85, valAxisMaxVal: 110, ...cf });
    const rx = 8.4;
    txt(s, "Drill from summary to source", { x: rx, y: 2.85, w: 4.3, h: 0.35, fontSize: 15, bold: true });
    const steps = [["KPI summary", "Value against plan and prior year"], ["Dimension split", "By business unit, department, vendor and more"], ["Source records", "Underlying documents, exportable to CSV"], ["Detail page", "One unit, vendor or customer in focus"]];
    line(s, rx + 0.2, 3.6, rx + 0.2, 5.5, { color: C.accent1, width: 1.5 });
    steps.forEach((st, i) => {
      const y = 3.35 + i * 0.68;
      circleNum(s, rx + 0.2, y + 0.2, 0.4, String(i + 1), C.accent1, 12);
      txt(s, [{ text: st[0], options: { fontSize: 12.5, bold: true, breakLine: true } }, { text: st[1], options: { fontSize: 11, color: C.accent4 } }], { x: rx + 0.6, y, w: 3.7, h: 0.6 });
    });
    txt(s, [{ text: "Also in the platform: ", options: { bold: true } }, { text: "Explain Change analysis, role-based access, shareable view links and an optional AI analyst with traceable answers." }],
      { x: rx, y: 6.1, w: 4.3, h: 0.8, fontSize: 11, color: C.accent4 });
    s.addNotes("Primary product slide. Capabilities shown (KPI cards vs plan/prior year, decomposition by dimension, records view with CSV export, detail pages, Explain Change, persona-based access, shareable URLs, AI analyst with 'How I computed this') are from the ELITIA BI functional specification. Connection to SGG's Odoo and mapping of SGG's business units into the BI semantic layer are proposed activities subject to technical validation in discovery. Mockup values are illustrative.");
  }

  // ================= 5 STAKEHOLDERS =================
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Solution" });
    eyebrow(s, "Executive reporting");
    s.addText("Executive reporting and business visibility", { placeholder: "title" });
    subtitle(s, "Management visibility, faster reporting and informed decisions at every level");
    const cx = [3.85, 6.9, 9.95], cw = 2.73;
    ["Finance", "HR", "Supply Chain"].forEach((h, i) => txt(s, h, { x: cx[i], y: 1.85, w: cw, h: 0.4, fontSize: 14, bold: true, color: C.accent1, valign: "middle" }));
    const lv = [
      ["Executive Management", "Consolidated performance and key indicators", C.text2],
      ["Department Heads", "Departmental performance, exceptions and trends", C.accent1],
      ["Operational Teams", "Detailed transactions and actionable information", C.accent4],
    ];
    const cells = [
      ["Revenue, expenses and profitability by business unit", "Headcount and payroll cost trends", "Procurement spend and inventory value"],
      ["Receivables and payables ageing, budget variance", "Attendance, overtime and absenteeism", "Stock levels and supplier delivery performance"],
      ["Invoices, journal entries and payment lines", "Employee attendance and timesheet records", "Purchase orders and stock movements"],
    ];
    lv.forEach((l, r) => {
      const y = 2.3 + r * 1.2;
      s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y, w: 3.0, h: 1.1, rectRadius: 0.15, fill: { color: l[2] }, line: { color: l[2], width: 0 } });
      txt(s, [{ text: l[0], options: { fontSize: 13, bold: true, breakLine: true } }, { text: l[1], options: { fontSize: 10.5 } }], { x: 0.85, y, w: 2.65, h: 1.1, valign: "middle", color: C.background1 });
      cells[r].forEach((c, k) => {
        s.addShape(S.ROUNDED_RECTANGLE, { x: cx[k], y, w: cw, h: 1.1, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: C.accent4, width: 1, dashType: "dash" } });
        txt(s, c, { x: cx[k] + 0.14, y, w: cw - 0.28, h: 1.1, fontSize: 12, valign: "middle" });
      });
    });
    txt(s, "Dashed boxes are illustrative KPI examples. The final KPI set will be agreed with SGG during discovery.", { x: 3.85, y: 5.95, w: 8.8, h: 0.28, fontSize: 10.5, italic: true, color: C.accent4 });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y: 6.3, w: 12.03, h: 0.7, rectRadius: 0.12, fill: { color: C.accent1, transparency: 90 }, line: { color: C.accent1, width: 1 } });
    txt(s, "Confirmed in ELITIA BI", { x: 0.85, y: 6.3, w: 2.8, h: 0.7, fontSize: 12, bold: true, color: C.accent1, valign: "middle" });
    const caps = ["KPI cards vs plan and prior year", "Drill-down to source records", "Role-based access to modules and data", "Shareable views and CSV export"];
    caps.forEach((c, i) => {
      const x = 3.85 + i * 2.2;
      s.addImage({ data: ic.check, x, y: 6.55, w: 0.2, h: 0.2 });
      txt(s, c, { x: x + 0.28, y: 6.3, w: 1.85, h: 0.7, fontSize: 10, valign: "middle" });
    });
    s.addNotes("Rows are stakeholder levels; columns are reporting areas. Dashed cells are illustrative KPI examples, not confirmed product features. The strip at the bottom lists capabilities confirmed in the ELITIA BI specification.");
  }

  // ================= 6 HEALTH CHECK =================
  pres.addSection({ title: "Workstreams" });
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Workstreams" });
    eyebrow(s, "Odoo health check");
    s.addText("Odoo ERP health check and UI/UX audit", { placeholder: "title" });
    subtitle(s, "Assess first, then recommend: improvements are prioritized from evidence");
    const st = [
      ["Review the environment", ["Current Odoo configuration", "Key business workflows"]],
      ["Understand the user experience", ["Usability issues and pain points", "Navigation and screen layouts"]],
      ["Identify gaps", ["Functional gaps", "Improvement opportunities"]],
      ["Prioritize", ["Ranked recommendations", "Agreed with SGG before any change"]],
    ];
    st.forEach((x, i) => {
      const px = 0.65 + i * 3.05;
      txt(s, "0" + (i + 1), { x: px, y: 1.9, w: 1.2, h: 0.8, fontSize: 38, bold: true, color: C.accent1 });
      txt(s, x[0], { x: px, y: 2.75, w: 2.8, h: 0.7, fontSize: 15, bold: true });
      txt(s, x[1].map((b, k) => ({ text: b, options: { bullet: true, breakLine: k < x[1].length - 1 } })), { x: px, y: 3.5, w: 2.8, h: 1.0, fontSize: 12, color: C.accent4, paraSpaceAfter: 4 });
    });
    txt(s, "The focus is user experience, adoption and process efficiency. No specific improvements are committed ahead of the assessment.", { x: 0.65, y: 4.7, w: 12.03, h: 0.35, fontSize: 12, italic: true, color: C.accent4 });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y: 5.25, w: 12.03, h: 1.65, rectRadius: 0.15, fill: { color: C.text2 }, line: { color: C.text2, width: 0 } });
    txt(s, "EXPECTED DELIVERABLES", { x: 0.95, y: 5.4, w: 5, h: 0.3, fontSize: 10.5, fontFace: SEMI, color: C.accent2, charSpacing: 4 });
    const dl = [["Odoo Health Check Report", ic.clip], ["UI/UX Assessment Findings", ic.eye], ["Gap & Improvement Register", ic.table], ["Prioritized Enhancement Roadmap", ic.map]];
    dl.forEach((d, i) => {
      const x = 0.95 + i * 2.93;
      s.addShape(S.OVAL, { x, y: 5.98, w: 0.6, h: 0.6, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 } });
      s.addImage({ data: d[1], x: x + 0.15, y: 6.13, w: 0.3, h: 0.3 });
      txt(s, d[0], { x: x + 0.75, y: 5.93, w: 2.05, h: 0.7, fontSize: 12, bold: true, color: C.background1, valign: "middle" });
    });
    s.addNotes("No improvements are promised before the assessment is complete.");
  }

  // ================= 7 MIGRATION =================
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Workstreams" });
    eyebrow(s, "Data migration");
    s.addText("Resort ERP to Odoo data migration", { placeholder: "title" });
    subtitle(s, "A six-step path from legacy extracts to signed-off data in Odoo");
    const steps = [
      ["Data Extraction", "Obtain historical data from Resort ERP in Excel format"],
      ["Data Assessment", "Review completeness, quality and consistency"],
      ["Data Cleansing", "Identify duplicates, missing values and inconsistencies"],
      ["Data Mapping", "Align legacy information with the relevant Odoo data structure"],
      ["Migration & Validation", "Load approved data into Odoo and validate the results"],
      ["Reconciliation & Sign‑off", "Obtain business confirmation before closure"],
    ];
    const dels = ["Source Excel extracts", "Data Assessment Report", "Cleansed Migration Files", "Data Mapping Document", "Migration Execution Report", "Data Reconciliation and Sign-off"];
    const col = (i) => 0.65 + i * 2.02;
    line(s, col(0) + 0.97, 2.3, col(5) + 0.97, 2.3, { color: C.accent1, width: 2 });
    steps.forEach((st, i) => {
      circleNum(s, col(i) + 0.97, 2.3, 0.6, String(i + 1), i === 5 ? C.text2 : C.accent1, 16);
      txt(s, st[0], { x: col(i), y: 2.8, w: 1.95, h: 0.65, fontSize: 12, bold: true, align: "center" });
      txt(s, st[1], { x: col(i) + 0.05, y: 3.55, w: 1.85, h: 1.35, fontSize: 11.5, color: C.accent4, align: "center" });
    });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y: 5.05, w: 12.03, h: 1.3, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: C.accent5, width: 1 }, shadow: shadow() });
    txt(s, "DELIVERABLES", { x: 0.85, y: 5.12, w: 3, h: 0.25, fontSize: 10, fontFace: SEMI, color: C.accent1, charSpacing: 4 });
    dels.forEach((d, i) => {
      txt(s, d, { x: col(i) + 0.05, y: 5.4, w: 1.85, h: 0.85, fontSize: 11.5, bold: i > 0, italic: i === 0, color: i === 0 ? C.accent4 : C.text1, align: "center", valign: "middle" });
    });
    s.addImage({ data: ic.info, x: 0.65, y: 6.58, w: 0.25, h: 0.25 });
    txt(s, "Final migration scope depends on available source data, historical period, data volume and the agreed Odoo objects.", { x: 1.05, y: 6.5, w: 11.6, h: 0.4, fontSize: 12, color: C.accent4, valign: "middle" });
    s.addNotes("Deliverables are aligned beneath the step that produces them. Extraction is client-provided Excel.");
  }

  // ================= 8 PAYROLL =================
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Workstreams" });
    eyebrow(s, "Payroll integration");
    s.addText("Automated payroll and time-tracking integration", { placeholder: "title" });
    subtitle(s, "From the biometric device to the bank upload");
    const f = [
      ["Biometric Devices", "Fingerprint / Facial Recognition", C.accent4],
      ["Attendance Data", "", C.accent1],
      ["Timesheet Validation", "", C.accent1],
      ["Payroll Processing in Odoo", "", C.text2],
      ["WPS File Generation", "", C.accent1],
      ["Bank Upload & Salary Disbursement", "", C.accent4],
    ];
    const acts = [
      "Assess existing biometric devices for integration",
      "Consolidate attendance data",
      "Align timesheet and payroll data",
      "Validate salary-related information",
      "Generate standard WPS files",
      "Test against applicable bank and WPS requirements",
    ];
    f.forEach((b, i) => {
      const x = 0.65 + i * 2.05;
      s.addShape(S.ROUNDED_RECTANGLE, { x, y: 2.0, w: 1.75, h: 1.4, rectRadius: 0.15, fill: { color: b[2] }, line: { color: b[2], width: 0 }, shadow: shadow() });
      const runs = [{ text: b[0], options: { fontSize: 12, bold: true, breakLine: !!b[1] } }];
      if (b[1]) runs.push({ text: "(" + b[1] + ")", options: { fontSize: 9.5 } });
      txt(s, runs, { x: x + 0.08, y: 2.0, w: 1.59, h: 1.4, align: "center", valign: "middle", color: C.background1 });
      if (i < 5) line(s, x + 1.78, 2.7, x + 2.04, 2.7, { color: C.accent4, width: 2, end: "triangle" });
      line(s, x + 0.875, 3.4, x + 0.875, 3.85, { color: C.accent4, width: 1, dash: "dash" });
      txt(s, acts[i], { x: x - 0.05, y: 3.9, w: 1.85, h: 1.3, fontSize: 11.5, align: "center" });
    });
    const lg = [[C.accent4, "SGG existing devices and bank process", 3.7], [C.accent1, "Proposed integration and configuration", 3.6], [C.text2, "Odoo", 1.0]];
    let lx = 0.65;
    lg.forEach((l) => {
      s.addShape(S.RECTANGLE, { x: lx, y: 5.42, w: 0.2, h: 0.2, fill: { color: l[0] }, line: { color: l[0], width: 0 } });
      txt(s, l[1], { x: lx + 0.3, y: 5.37, w: l[2], h: 0.3, fontSize: 10.5, color: C.accent4, valign: "middle" });
      lx += 0.3 + l[2] + 0.2;
    });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y: 5.95, w: 12.03, h: 0.95, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: C.accent5, width: 1 }, shadow: shadow() });
    s.addImage({ data: ic.info, x: 0.9, y: 6.3, w: 0.25, h: 0.25 });
    txt(s, [{ text: "Design depends on: ", options: { bold: true } }, { text: "biometric device compatibility, Odoo payroll configuration, payroll rules and bank-specific WPS specifications. These are confirmed during discovery." }],
      { x: 1.4, y: 5.95, w: 11.1, h: 0.95, fontSize: 12, valign: "middle" });
    s.addNotes("Conceptual flow only. WPS file format is validated against the bank and WPS requirements that apply to SGG.");
  }

  // ================= 9 ROADMAP =================
  pres.addSection({ title: "Implementation" });
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Implementation" });
    eyebrow(s, "Implementation");
    s.addText("Implementation approach and delivery roadmap", { placeholder: "title" });
    subtitle(s, "Five phases. Timelines will be confirmed in discovery and mutually agreed.");
    txt(s, "PHASE", { x: 0.65, y: 1.85, w: 2.5, h: 0.25, fontSize: 10, fontFace: SEMI, color: C.accent4, charSpacing: 3 });
    txt(s, "SEQUENCE (INDICATIVE)", { x: 3.45, y: 1.85, w: 3.4, h: 0.25, fontSize: 10, fontFace: SEMI, color: C.accent4, charSpacing: 3 });
    txt(s, "KEY ACTIVITIES", { x: 7.2, y: 1.85, w: 5.4, h: 0.25, fontSize: 10, fontFace: SEMI, color: C.accent4, charSpacing: 3 });
    const ph = [
      ["Discovery & Assessment", "Requirement workshops · Odoo environment review · BI reporting requirements · Integration and data assessment"],
      ["Solution Design", "Dashboard and KPI design · Odoo improvement recommendations · Migration mapping · Integration design"],
      ["Configuration & Implementation", "ELITIA BI configuration and dashboards · Approved Odoo enhancements · Data migration · Payroll and attendance integration"],
      ["Testing & Deployment", "Functional testing · Data reconciliation · User acceptance testing · Deployment and handover"],
      ["Stabilization & Support", "Post-deployment assistance · Issue resolution · Knowledge transfer"],
    ];
    ph.forEach((p, i) => {
      const y = 2.15 + i * 0.77;
      line(s, 0.65, y, 12.68, y, { color: C.accent5, width: 1.25 });
      txt(s, p[0], { x: 0.65, y: y + 0.03, w: 2.7, h: 0.7, fontSize: 12.5, bold: true, valign: "middle" });
      const bx = 3.45 + i * 0.55;
      s.addShape(S.ROUNDED_RECTANGLE, { x: bx, y: y + 0.17, w: 1.1, h: 0.4, rectRadius: 0.2, fill: { color: i === 4 ? C.text2 : C.accent1 }, line: { color: C.background1, width: 0 } });
      txt(s, "Phase " + (i + 1), { x: bx, y: y + 0.17, w: 1.1, h: 0.4, fontSize: 10.5, bold: true, color: C.background1, align: "center", valign: "middle" });
      txt(s, p[1], { x: 7.2, y: y + 0.03, w: 5.48, h: 0.7, fontSize: 11, valign: "middle" });
    });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.65, y: 6.1, w: 12.03, h: 0.85, rectRadius: 0.15, fill: { color: C.accent1, transparency: 90 }, line: { color: C.accent1, width: 1 } });
    txt(s, [{ text: "Future readiness", options: { bold: true, color: C.accent1, breakLine: true } }, { text: "Odoo v20 upgrade, planned 2027", options: { bold: true } }], { x: 0.9, y: 6.1, w: 3.4, h: 0.85, fontSize: 12.5, valign: "middle" });
    txt(s, "The architecture and integrations will be designed for maintainability and upgrade compatibility. Compatibility with Odoo v20 will be validated technically and is not assumed in advance.", { x: 4.5, y: 6.1, w: 8.0, h: 0.85, fontSize: 11, valign: "middle" });
    s.addNotes("No durations are stated. Bars show sequence only. v20 compatibility is not guaranteed before technical validation.");
  }

  // ================= 10 COMMERCIALS =================
  pres.addSection({ title: "Commercials" });
  {
    const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Commercials" });
    eyebrow(s, "Commercials");
    s.addText("Commercials, resources and terms and conditions", { placeholder: "title" });
    const H = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: "1F497D" }, fontSize: 10, valign: "middle" } });
    const P = (t) => ({ text: t, options: { bold: true, color: "F78B15", fontSize: 10, valign: "middle" } });
    const T = (t, b) => ({ text: t, options: { color: "141E2D", bold: !!b, fontSize: 10, valign: "middle" } });
    const tb = { type: "solid", pt: 0.5, color: "DCE1E6" };
    txt(s, "A   Commercial proposal", { x: 0.65, y: 1.5, w: 5.3, h: 0.35, fontSize: 13, bold: true, color: C.accent1, valign: "middle" });
    s.addTable([
      [H("Item"), H("Amount")],
      [T("Professional services and implementation charges"), P("[Amount]")],
      [T("ELITIA BI licensing / subscription, if applicable"), P("[Amount]")],
      [T("Third-party or infrastructure costs, if applicable"), P("[Amount]")],
      [T("Applicable taxes"), P("[Rate / amount]")],
      [T("Payment milestones and schedule"), P("[Milestone, % and due date]")],
    ], { x: 0.65, y: 1.9, w: 5.3, colW: [3.0, 2.3], rowH: 0.43, border: tb, margin: [0, 0.08, 0, 0.08] });
    txt(s, "B   Proposed manpower resources", { x: 6.2, y: 1.5, w: 6.5, h: 0.35, fontSize: 13, bold: true, color: C.accent1, valign: "middle" });
    const roles = [
      ["Project Manager / Engagement Lead", "Delivery governance and coordination"],
      ["ELITIA BI / BI Consultant", "KPI and dashboard configuration"],
      ["Odoo Functional Consultant", "Health check, UI/UX and payroll setup"],
      ["Data Migration Specialist", "Cleansing, mapping and loading"],
      ["Integration Consultant", "Odoo, biometric and WPS integration"],
      ["QA / Testing Support", "Test execution and UAT support"],
    ];
    s.addTable([[H("Role"), H("Key responsibility"), H("Allocation")], ...roles.map((r) => [T(r[0], true), T(r[1]), P("[Days / %]")])],
      { x: 6.2, y: 1.9, w: 6.48, colW: [2.5, 2.88, 1.1], rowH: 0.43, border: tb, margin: [0, 0.08, 0, 0.08] });
    txt(s, "C   Terms & conditions", { x: 0.65, y: 5.05, w: 6, h: 0.35, fontSize: 13, bold: true, color: C.accent1, valign: "middle" });
    const terms = [
      ["Scope and deliverables: ", "based on mutually approved requirements."],
      ["Timelines: ", "subject to discovery and scope confirmation."],
      ["Client responsibilities: ", "timely access, data, infrastructure and approvals."],
      ["Change requests: ", "additional scope is estimated and agreed before work begins."],
      ["Third-party dependencies: ", "licensing and external services remain subject to the provider's terms."],
      ["Payment terms: ", "as per the milestone schedule in Section A."],
      ["Acceptance and sign-off: ", "deliverables are confirmed through written client sign-off."],
      ["Warranty and support: ", "post-go-live support as agreed commercially: [duration]."],
    ];
    [0, 1].forEach((c) => {
      const items = terms.slice(c * 4, c * 4 + 4);
      txt(s, items.flatMap((t, k) => [
        { text: t[0], options: { bold: true } },
        { text: t[1], options: { breakLine: k < items.length - 1 } },
      ]), { x: 0.65 + c * 6.2, y: 5.45, w: 5.85, h: 1.55, fontSize: 10, paraSpaceAfter: 4 });
    });
    s.addNotes("Only slide with commercial and contractual content. All amounts, allocations and the support duration are editable placeholders (orange text). No prices, names or commitments have been invented.");
  }

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("done");
})();
