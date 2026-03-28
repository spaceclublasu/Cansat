// ─── Hello , This code is non functional , note this is just the telemtry simulation
// page, just laying it out here........... ─────

function TelemetrySection() {
  const altDrift = useRef(2.8);
  const [isLive, setIsLive] = useState(true);
  const [phase, setPhase] = useState("ASCENT");
  const [elapsed, setElapsed] = useState(0);

  const [alt, setAlt] = useState(() => makeSeries(80, 25));
  const [temp, setTemp] = useState(() => makeSeries(29, 3));
  const [pressure, setPressure] = useState(() => makeSeries(1013, 5));
  const [humidity, setHumidity] = useState(() => makeSeries(61, 7));
  const [accelX, setAccelX] = useState(() => makeSeries(.1, 1.1));
  const [accelY, setAccelY] = useState(() => makeSeries(.05, .8));
  const [light, setLight] = useState(() => makeSeries(410, 75));
  const [rssi, setRssi] = useState(() => makeSeries(-71, 4));

  const doReset = () => {
    setAlt(makeSeries(80, 25)); setTemp(makeSeries(29, 3));
    setPressure(makeSeries(1013, 5)); setHumidity(makeSeries(61, 7));
    setAccelX(makeSeries(.1, 1.1)); setAccelY(makeSeries(.05, .8));
    setLight(makeSeries(410, 75)); setRssi(makeSeries(-71, 4));
    setElapsed(0); altDrift.current = 2.8; setPhase("ASCENT");
  };

  useEffect(() => {
    if (!isLive) return;
    const id = setInterval(() => {
      setElapsed(e => e + 1);
      setAlt(prev => {
        const last = prev[prev.length - 1].v;
        if (last > 920) { altDrift.current = -3.8; setPhase("DESCENT"); }
        if (last < 8 && altDrift.current < 0) { altDrift.current = 0; setPhase("LANDED"); }
        return addPoint(prev, 80, 16, altDrift.current);
      });
      setTemp(prev => addPoint(prev, 29, 1.2, -.04));
      setPressure(prev => addPoint(prev, 1013, 1.8, -.07));
      setHumidity(prev => addPoint(prev, 61, 2.2, .02));
      setAccelX(prev => addPoint(prev, .1, 1.6));
      setAccelY(prev => addPoint(prev, .05, 1.1));
      setLight(prev => addPoint(prev, 410, 55));
      setRssi(prev => addPoint(prev, -71, 2.5));
    }, 750);
    return () => clearInterval(id);
  }, [isLive]);

  const L = {
    alt: alt[alt.length - 1]?.v.toFixed(1),
    temp: temp[temp.length - 1]?.v.toFixed(1),
    pressure: pressure[pressure.length - 1]?.v.toFixed(1),
    humidity: humidity[humidity.length - 1]?.v.toFixed(1),
    accelX: accelX[accelX.length - 1]?.v.toFixed(2),
    accelY: accelY[accelY.length - 1]?.v.toFixed(2),
    light: light[light.length - 1]?.v.toFixed(0),
    rssi: rssi[rssi.length - 1]?.v.toFixed(0),
  };

  const phaseCol = { ASCENT: C.green, DESCENT: C.accent, LANDED: C.blue, STANDBY: C.muted };
  const pCol = phaseCol[phase] || C.muted;

  const topCards = [
    { label: "Altitude", val: L.alt, unit: "m", color: C.green, icon: "↑" },
    { label: "Temperature", val: L.temp, unit: "°C", color: "#FF6B6B", icon: "🌡" },
    { label: "Pressure", val: L.pressure, unit: "hPa", color: C.blue, icon: "⬤" },
    { label: "Signal (RSSI)", val: L.rssi, unit: "dBm", color: C.purple, icon: "📶" },
  ];

  const subCharts = [
    { label: "Temperature", data: temp, color: "#FF6B6B", unit: "°C", val: L.temp },
    { label: "Pressure", data: pressure, color: C.blue, unit: "hPa", val: L.pressure },
    { label: "Humidity", data: humidity, color: C.cyan, unit: "%", val: L.humidity },
    { label: "Accel X", data: accelX, color: C.yellow, unit: "g", val: L.accelX },
    { label: "Accel Y", data: accelY, color: C.accentSoft, unit: "g", val: L.accelY },
    { label: "Light", data: light, color: "#FFD700", unit: "lux", val: L.light },
    { label: "RSSI", data: rssi, color: C.purple, unit: "dBm", val: L.rssi },
    { label: "Humidity", data: humidity, color: C.cyan, unit: "%", val: L.humidity },
  ];

  // Use only 6 to keep layout clean
  const shownCharts = subCharts.slice(0, 6);

  return (
    <section style={{ padding: "90px clamp(14px,4vw,60px)" }}>
      <div style={{ maxWidth: 1280, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16, marginBottom: 36 }}>
          <div>
            <SLabel text="Live Telemetry Dashboard" />
            <h2 style={{ fontFamily: "'Syne',sans-serif", fontSize: "clamp(26px,3.6vw,50px)", fontWeight: 800, color: C.white, margin: "0 0 8px" }}>
              Mission <span style={{ color: C.accent }}>Data Stream</span>
            </h2>
            <p style={{ fontFamily: "'DM Sans',sans-serif", fontSize: 14, color: C.muted }}>
              Real-time time-series sensor data streamed via LoRa telemetry link · simulated feed
            </p>
          </div>
          {/* Controls */}
          <div style={{ display: "flex", flexDirection: "column", gap: 9, minWidth: 210 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "9px 14px", background: C.bgCard, border: `1px solid ${pCol}44`, borderRadius: 8 }}>
              <div className="live-dot" style={{ width: 7, height: 7, borderRadius: "50%", background: isLive ? pCol : C.muted, flexShrink: 0 }} />
              <span style={{ fontFamily: "'Space Mono',monospace", fontSize: 10, color: pCol, letterSpacing: 1 }}>{isLive ? `● ${phase}` : "⏸ PAUSED"}</span>
              <div style={{ marginLeft: "auto", fontFamily: "'Space Mono',monospace", fontSize: 9, color: C.muted }}>T+{elapsed}s</div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => setIsLive(l => !l)} style={{ flex: 1, padding: "8px 10px", borderRadius: 6, border: `1px solid ${isLive ? C.red + "88" : C.green + "88"}`, background: "transparent", color: isLive ? C.red : C.green, fontFamily: "'Space Mono',monospace", fontSize: 9, cursor: "pointer", letterSpacing: .8 }}>{isLive ? "⏸ Pause" : "▶ Resume"}</button>
              <button onClick={doReset} style={{ flex: 1, padding: "8px 10px", borderRadius: 6, border: `1px solid ${C.border}`, background: "transparent", color: C.muted, fontFamily: "'Space Mono',monospace", fontSize: 9, cursor: "pointer", letterSpacing: .8 }}>↺ Reset</button>
            </div>
          </div>
        </div>

        {/* Top summary cards */}
        <div className="tele-top-row" style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 20 }}>
          {topCards.map(s => (
            <HoverCard key={s.label} glowColor={s.color + "55"} style={{ padding: "14px 15px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
                <div style={{ width: 36, height: 36, borderRadius: 8, background: s.color + "18", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, flexShrink: 0 }}>{s.icon}</div>
                <div>
                  <div style={{ fontFamily: "'Space Mono',monospace", fontSize: 9, color: C.muted, letterSpacing: 1.4, marginBottom: 3, textTransform: "uppercase" }}>{s.label}</div>
                  <div style={{ fontFamily: "'Syne',sans-serif", fontSize: "clamp(15px,1.8vw,21px)", fontWeight: 700, color: s.color }}>{s.val}<span style={{ fontSize: 10, color: C.muted, marginLeft: 3 }}>{s.unit}</span></div>
                </div>
              </div>
            </HoverCard>
          ))}
        </div>

        {/* Main Altitude chart */}
        <HoverCard glowColor={C.green + "44"} style={{ padding: "22px 22px 14px", marginBottom: 18 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 10, marginBottom: 10 }}>
            <div>
              <div style={{ fontFamily: "'Syne',sans-serif", fontSize: 16, fontWeight: 700, color: C.white }}>Altitude — Time Series</div>
              <div style={{ fontFamily: "'DM Sans',sans-serif", fontSize: 12, color: C.muted }}>Primary mission parameter: ascent & descent arc</div>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <Badge color={C.green}>Current: {L.alt} m</Badge>
              <Badge color={pCol}>{phase}</Badge>
            </div>
          </div>
          <LineChart data={alt} color={C.green} unit="m" label="Altitude" height={180} />
        </HoverCard>

        {/* Secondary charts 3-column */}
        <div className="tele-secondary" style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14 }}>
          {shownCharts.map(ch => (
            <HoverCard key={ch.label + ch.color} glowColor={ch.color + "44"} style={{ padding: "16px 16px 10px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                <div>
                  <div style={{ fontFamily: "'Space Mono',monospace", fontSize: 9, color: C.muted, letterSpacing: 1.4, textTransform: "uppercase", marginBottom: 3 }}>{ch.label}</div>
                  <div style={{ fontFamily: "'Syne',sans-serif", fontSize: 20, fontWeight: 700, color: ch.color }}>{ch.val}<span style={{ fontSize: 11, color: C.muted, marginLeft: 3 }}>{ch.unit}</span></div>
                </div>
              </div>
              <LineChart data={ch.data} color={ch.color} unit={ch.unit} label={ch.label} height={140} />
            </HoverCard>
          ))}
        </div>

        {/* Raw packet readout */}
        <div style={{ marginTop: 16, background: C.bgCardAlt, border: `1px solid ${C.border}`, borderRadius: 8, padding: "12px 16px", fontFamily: "'Space Mono',monospace", fontSize: 11, color: C.green, overflowX: "auto", whiteSpace: "nowrap" }}>
          <span style={{ color: C.muted, marginRight: 10 }}>PACKET ›</span>
          ALT:{L.alt}m · TMP:{L.temp}°C · PRE:{L.pressure}hPa · HUM:{L.humidity}% · AX:{L.accelX}g · AY:{L.accelY}g · LUX:{L.light} · RSSI:{L.rssi}dBm · T+{elapsed}s · {phase}
        </div>
      </div>
    </section>
  );
} 
