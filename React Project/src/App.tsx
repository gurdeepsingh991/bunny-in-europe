import { useState } from "react";
import "./App.css";

function App() {
  const [hasTraveled, setHasTraveled] = useState<string>("no");
  const [selectedCountries, setSelectedCountries] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [showResults, setShowResults] = useState<boolean>(false)
  const countries = ["Natherlands", "Paris", "France", "Itely"];

  const handleTravelQuestionChange = (value: string) => {
    setHasTraveled(value);
    setResult([])
    setShowResults(false)

    if (value === "no") {
      setSelectedCountries([]);
    }
  };

  const handleCountrySelect = (country: string) => {
    if (selectedCountries.includes(country)) {
      setSelectedCountries(selectedCountries.filter((c) => c !== country));
    } else {
      setSelectedCountries([...selectedCountries, country]);
    }
  };

  const createTravel = async () => {
    await fetch("http://127.0.0.1:8000/api/travel/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        has_traveled_toeurope: hasTraveled === "yes",
        countries: selectedCountries,
      }),
    });


    const response = await fetch("http://127.0.0.1:8000/api/travel/");
    const data = await response.json();

    setShowResults(true)
    setResult(data);
  };

  return (
    <>
      <h1>Has "Bunny" been to Europe before?</h1>
      <label>
        <input
          type="radio"
          value="yes"
          defaultChecked={hasTraveled === "yes"}
          name="hasTraveled"
          onChange={(e) => handleTravelQuestionChange(e.target.value)}
        />
        Yes
      </label>
      <label>
        <input
          type="radio"
          value="no"
          name="hasTraveled"
          defaultChecked={hasTraveled === "no"}
          onChange={(e) => handleTravelQuestionChange(e.target.value)}
        />
        No
      </label>

      {hasTraveled &&
        hasTraveled == "yes" &&
        countries.map((country, index) => (
          <div key={index}>
            <label>
              <input
                type="checkbox"
                onChange={() => handleCountrySelect(country)}
                checked={selectedCountries.includes(country)}
                value={country}
                name="hasTraveled"
              />
              {country}
            </label>
          </div>
        ))}
      <div>
        <button onClick={createTravel}> Submit</button>
      </div>

      {result && showResults && (
        <div>
          {result.has_traveled_toeurope ? (
            <>
              <h2>The countries "Bunny" has been to in Europe:</h2>
              <ul>
                {result.countries?.map((country: string, index: number) => (
                  <li key={index}>{country}</li>
                ))}
              </ul>
            </>
          ) : (
            <h2>"Bunny" has never been to Europe.</h2>
          )}
        </div>
      )}
    </>
  );
}

export default App;
