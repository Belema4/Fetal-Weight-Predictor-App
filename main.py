import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export default function FetalWeightPredictor() {
  const [sfh, setSfh] = useState(0);
  const [proteinuria, setProteinuria] = useState("");
  const [fbs, setFbs] = useState(0);
  const [bp, setBp] = useState({ systolic: 0, diastolic: 0 });
  const [gestationalAge, setGestationalAge] = useState(28);
  const [result, setResult] = useState(null);

  // Estimate fetal weight (Hadlock formula simplified)
  const estimateFetalWeight = (sfh) => +(sfh * 0.09).toFixed(2);

  // Clinical Standards (WHO macrosomia ≥4.0kg, ACOG pre-eclampsia criteria)
  const standards = {
    fbs: {
      normal: "< 5.1 mmol/L (ACOG)",
      impaired: "5.1–6.9 mmol/L",
      gdm: "≥ 7.0 mmol/L (WHO)"
    },
    bp: {
      normal: "< 140/90 mmHg",
      preeclampsia: "≥ 140/90 mmHg + proteinuria/symptoms"
    },
    fetal: {
      macrosomia: "≥ 4.0 kg (WHO)",  // Updated threshold
      fgr: `< 2.5 kg or < ${calculatePercentile(2.5)}%ile for ${gestationalAge} weeks`
    }
  };

  // Growth percentiles (simplified Hadlock curves)
  const calculatePercentile = (weight) => {
    const percentiles = {
      24: { p10: 0.6, p50: 0.7, p90: 0.8 },
      28: { p10: 1.0, p50: 1.2, p90: 1.4 },
      32: { p10: 1.6, p50: 1.9, p90: 2.2 },
      36: { p10: 2.4, p50: 2.9, p90: 3.3 },
      40: { p10: 2.9, p50: 3.5, p90: 4.1 }
    };
    
    const week = Math.min(40, Math.max(24, gestationalAge));
    const data = percentiles[week];
    
    if (weight < data.p10) return "<10";
    if (weight >= data.p90) return ">90";
    return "10-90";
  };

  // Predict outcomes with clinical standards
  const predictOutcome = (weight, proteinuria, fbs, bp) => {
    const percentile = calculatePercentile(weight);
    let outcome = `Appropriate Growth (${percentile}%ile)`;
    
    // WHO macrosomia standard (≥4.0kg)
    if (weight >= 4.0) outcome = `Macrosomia (WHO ≥ 4.0 kg, ${percentile}%ile)`;
    else if (weight < 2.5 || percentile === "<10") outcome = `Possible FGR (${percentile}%ile)`;

    let risks = [];
    let recommendations = [];
    
    // Proteinuria & BP (Pre-eclampsia)
    if (["++", "+++", "++++"].includes(proteinuria)) {
      risks.push("ACOG: Significant Proteinuria (≥2+)");
      if (bp.systolic >= 140 || bp.diastolic >= 90) {
        risks.push(`ACOG: Pre-eclampsia (BP ${bp.systolic}/${bp.diastolic} mmHg)`);
        recommendations.push("Urgent OB evaluation + labs (CBC, LFTs, creatinine)");
      }
    } else if (bp.systolic >= 140 || bp.diastolic >= 90) {
      risks.push("ACOG: Gestational Hypertension");
    }

    // FBS (GDM)
    if (fbs >= 7.0) {
      risks.push("WHO: Gestational Diabetes (FBS ≥7.0 mmol/L)");
      recommendations.push("1. 75g OGTT confirmation\n2. Diabetes education\n3. Glucose monitoring");
    } else if (fbs >= 5.1) {
      risks.push("ACOG: Impaired Fasting Glucose");
      recommendations.push("Consider 1-hour 50g glucose challenge test");
    }

    // Growth abnormalities
    if (weight >= 4.0) {
      recommendations.push("• Ultrasound for growth verification\n• Monitor for shoulder dystocia");
    } else if (percentile === "<10") {
      recommendations.push("• Doppler ultrasound\n• Antenatal testing\n• Consider delivery at 37-38 weeks if severe");
    }

    return { 
      weight, 
      outcome, 
      risks, 
      recommendations,
      percentile 
    };
  };

  const handleSubmit = () => {
    const weight = estimateFetalWeight(sfh);
    const prediction = predictOutcome(weight, proteinuria, fbs, bp);
    setResult(prediction);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">
        Fetal Weight Predictor (WHO/ACOG Standards)
      </h1>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Input Section */}
        <Card>
          <CardContent className="space-y-4 p-6">
            <Input
              type="number"
              placeholder="Symphysis-Fundal Height (cm)"
              value={sfh}
              onChange={(e) => setSfh(+e.target.value)}
            />
            
            <Input
              type="number"
              placeholder="Gestational Age (weeks)"
              min="24"
              max="42"
              value={gestationalAge}
              onChange={(e) => setGestationalAge(+e.target.value)}
            />
            
            <Input
              type="text"
              placeholder="Proteinuria (+, ++, +++, -)"
              value={proteinuria}
              onChange={(e) => setProteinuria(e.target.value)}
            />
            
            <Input
              type="number"
              step="0.1"
              placeholder="Fasting Blood Sugar (mmol/L)"
              value={fbs}
              onChange={(e) => setFbs(+e.target.value)}
              className={
                fbs >= 7.0 ? "border-2 border-red-500" : 
                fbs >= 5.1 ? "border-2 border-yellow-500" : ""
              }
            />
            
            <div className="grid grid-cols-2 gap-2">
              <Input
                type="number"
                placeholder="Systolic BP (mmHg)"
                value={bp.systolic}
                onChange={(e) => setBp({...bp, systolic: +e.target.value})}
                className={bp.systolic >= 140 ? "border-2 border-red-500" : ""}
              />
              <Input
                type="number"
                placeholder="Diastolic BP (mmHg)"
                value={bp.diastolic}
                onChange={(e) => setBp({...bp, diastolic: +e.target.value})}
                className={bp.diastolic >= 90 ? "border-2 border-red-500" : ""}
              />
            </div>
            
            <Button onClick={handleSubmit} className="w-full bg-blue-600 hover:bg-blue-700">
              Calculate
            </Button>
          </CardContent>
        </Card>

        {/* Results Section */}
        {result && (
          <Card className="border-blue-200">
            <CardContent className="p-6 space-y-4">
              <div className="space-y-2">
                <h2 className="font-bold text-lg text-blue-800">Results</h2>
                <div className="grid grid-cols-2 gap-2">
                  <p>Weight: <strong>{result.weight} kg</strong></p>
                  <p>Percentile: <strong>{result.percentile}</strong></p>
                </div>
                <p className="font-medium">{result.outcome}</p>
              </div>
              
              {result.risks.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-bold text-red-700">Clinical Risks</h3>
                  <ul className="list-disc pl-5 space-y-1">
                    {result.risks.map((risk, i) => (
                      <li key={i} className={risk.includes("Pre-eclampsia") || risk.includes("Diabetes") ? "font-semibold" : ""}>
                        {risk}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {result.recommendations.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-bold text-green-700">Recommendations</h3>
                  <ul className="list-decimal pl-5 space-y-1">
                    {result.recommendations.map((rec, i) => (
                      <li key={i} className="text-sm">{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="space-y-2">
                <h3 className="font-bold">Growth Percentiles</h3>
                <Table className="border">
                  <TableHeader className="bg-gray-100">
                    <TableRow>
                      <TableHead>Week</TableHead>
                      <TableHead>10%ile</TableHead>
                      <TableHead>50%ile</TableHead>
                      <TableHead>90%ile</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {[24, 28, 32, 36, 40].map((week) => (
                      <TableRow 
                        key={week} 
                        className={week === gestationalAge ? "bg-blue-50" : ""}
                      >
                        <TableCell>{week}</TableCell>
                        <TableCell>{(week*0.1 + 0.4).toFixed(1)} kg</TableCell>
                        <TableCell>{(week*0.1 + 0.7).toFixed(1)} kg</TableCell>
                        <TableCell>{(week*0.1 + 1.1).toFixed(1)} kg</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
      
      {/* Standards Reference */}
      <Card className="mt-6 border-gray-200">
        <CardContent className="p-6">
          <h2 className="font-bold mb-3 text-gray-700">Clinical Standards</h2>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div>
              <h3 className="font-semibold">Fetal Growth</h3>
              <ul className="space-y-1">
                <li>• Macrosomia: <strong>≥4.0 kg (WHO)</strong></li>
                <li>• FGR: <strong>&lt;{calculatePercentile(2.5)}%ile</strong></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold">Glucose</h3>
              <ul className="space-y-1">
                <li>• Normal: <strong>&lt;5.1 mmol/L</strong></li>
                <li>• GDM: <strong>≥7.0 mmol/L (WHO)</strong></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold">Blood Pressure</h3>
              <ul className="space-y-1">
                <li>• Normal: <strong>&lt;140/90 mmHg</strong></li>
                <li>• Pre-eclampsia: <strong>≥140/90 + proteinuria</strong></li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
