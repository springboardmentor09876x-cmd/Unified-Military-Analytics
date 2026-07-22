const customNeonColors = ['#00F0FF', '#FF007F', '#FFD60A', '#B829EA', '#39FF14', '#FF5733'];
const chartBg = 'rgba(18, 19, 28, 0.6)';

let militaryData = [];

// DOM Elements
const viewRadios = document.querySelectorAll('input[name="view"]');
const quickStatsSection = document.getElementById('quick-stats');
const nationOverviewSection = document.getElementById('nation-overview');

// Quick Stats DOM
const continentFilter = document.getElementById('continent-filter');
const regionFilter = document.getElementById('region-filter');
const totalBudgetEl = document.getElementById('total-budget');
const totalManpowerEl = document.getElementById('total-manpower');
const totalAssetsEl = document.getElementById('total-assets');
const topRankedCountryEl = document.getElementById('top-ranked-country');
const topRankedPiEl = document.getElementById('top-ranked-pi');

// Nation Overview DOM
const countryInput = document.getElementById('country-input');
const countryList = document.getElementById('country-list');
const noPowerIndexEl = document.getElementById('no-power-index');
const noRankEl = document.getElementById('no-rank');
const noDefenseBudgetEl = document.getElementById('no-defense-budget');
const noActivePersonnelEl = document.getElementById('no-active-personnel');
const noTotalAssetsEl = document.getElementById('no-total-assets');


// Format functions
function formatBudget(value) {
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    return `$${value.toLocaleString(undefined, {maximumFractionDigits: 0})}`;
}

function formatNumber(value) {
    return value.toLocaleString(undefined, {maximumFractionDigits: 0});
}

// Fetch data
fetch('military_data.json')
    .then(response => response.json())
    .then(data => {
        militaryData = data;
        initApp();
    })
    .catch(error => {
        console.error("Error loading military_data.json", error);
    });

function initApp() {
    setupViewToggle();
    setupSidebarToggle();
    initQuickStats();
    initNationOverview();
}

function setupSidebarToggle() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');
    
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        // trigger resize for plotly to adapt to new width
        setTimeout(() => window.dispatchEvent(new Event('resize')), 300);
    });
}

function setupViewToggle() {
    viewRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'Quick Stats') {
                quickStatsSection.classList.add('active');
                nationOverviewSection.classList.remove('active');
                // Trigger resize for plotly
                window.dispatchEvent(new Event('resize'));
            } else {
                quickStatsSection.classList.remove('active');
                nationOverviewSection.classList.add('active');
                window.dispatchEvent(new Event('resize'));
            }
        });
    });
}

// --- QUICK STATS ---

function initQuickStats() {
    // Populate Continents
    const continents = [...new Set(militaryData.map(d => String(d.continent)).filter(c => c !== 'nan' && c !== ''))].sort();
    continentFilter.innerHTML = '<option value="All">All</option>';
    continents.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        continentFilter.appendChild(opt);
    });

    continentFilter.addEventListener('change', () => {
        updateRegionFilter();
        updateQuickStats();
    });
    
    regionFilter.addEventListener('change', updateQuickStats);

    updateRegionFilter();
    updateQuickStats();
}

function updateRegionFilter() {
    const selectedContinent = continentFilter.value;
    let filtered = militaryData;
    if (selectedContinent !== 'All') {
        filtered = militaryData.filter(d => d.continent === selectedContinent);
    }
    
    const regions = [...new Set(filtered.map(d => String(d.region)).filter(r => r !== 'nan' && r !== ''))].sort();
    
    const prevRegion = regionFilter.value;
    
    regionFilter.innerHTML = '<option value="All">All</option>';
    regions.forEach(r => {
        const opt = document.createElement('option');
        opt.value = r;
        opt.textContent = r;
        regionFilter.appendChild(opt);
    });
    
    if (regions.includes(prevRegion)) {
        regionFilter.value = prevRegion;
    }
}

function updateQuickStats() {
    const selectedContinent = continentFilter.value;
    const selectedRegion = regionFilter.value;
    
    let filtered = militaryData;
    if (selectedContinent !== 'All') {
        filtered = filtered.filter(d => d.continent === selectedContinent);
    }
    if (selectedRegion !== 'All') {
        filtered = filtered.filter(d => d.region === selectedRegion);
    }
    
    // Update KPIs
    const totalBudget = filtered.reduce((sum, d) => sum + (d.defense_budget_usd || 0), 0);
    const totalManpower = filtered.reduce((sum, d) => sum + (d.total_military_manpower || 0), 0);
    const totalAssets = filtered.reduce((sum, d) => sum + (d.total_military_assets || 0), 0);
    
    totalBudgetEl.textContent = formatBudget(totalBudget);
    totalManpowerEl.textContent = formatNumber(totalManpower);
    totalAssetsEl.textContent = formatNumber(totalAssets);
    
    if (filtered.length > 0) {
        let bestCountry = filtered[0];
        for (let i = 1; i < filtered.length; i++) {
            if (filtered[i].power_index < bestCountry.power_index && filtered[i].power_index !== 0) {
                bestCountry = filtered[i];
            } else if (bestCountry.power_index === 0 && filtered[i].power_index !== 0) {
                bestCountry = filtered[i];
            }
        }
        topRankedCountryEl.textContent = bestCountry.country;
        topRankedPiEl.textContent = `PI: ${bestCountry.power_index.toFixed(4)}`;
    } else {
        topRankedCountryEl.textContent = "N/A";
        topRankedPiEl.textContent = "PI: 0.0000";
    }
    
    drawTop10Chart(filtered);
    drawDonutChart(filtered);
}

function drawTop10Chart(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('bar-chart');
        return;
    }
    
    let sorted = [...filtered].sort((a, b) => (b.budget_to_gdp_ratio || 0) - (a.budget_to_gdp_ratio || 0));
    let top10 = sorted.slice(0, 10).reverse(); // Reverse for plotly horizontal bar
    
    const trace = {
        x: top10.map(d => d.budget_to_gdp_ratio),
        y: top10.map(d => d.country),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: [
                '#FF007F', '#00F0FF', '#FFD60A', '#B829EA', '#39FF14',
                '#FF5733', '#FF00FF', '#00FF00', '#FFFF00', '#00FFFF'
            ],
            line: {width: 0},
            opacity: 0.9
        }
    };
    
    const layout = {
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        margin: { l: 100, r: 20, t: 10, b: 40 },
        xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
        yaxis: { gridcolor: 'rgba(255,255,255,0.1)' }
    };
    
    Plotly.newPlot('bar-chart', [trace], layout, {responsive: true});
}

function drawDonutChart(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('donut-chart');
        return;
    }
    
    // Aggregate by continent
    const agg = {};
    filtered.forEach(d => {
        const c = d.continent || 'Unknown';
        if (!agg[c]) agg[c] = 0;
        agg[c] += (d.total_military_assets || 0);
    });
    
    const labels = Object.keys(agg);
    const values = Object.values(agg);
    
    const trace = {
        labels: labels,
        values: values,
        type: 'pie',
        hole: 0.6,
        textinfo: 'percent',
        textposition: 'inside',
        marker: {
            colors: customNeonColors,
            line: { color: '#12131C', width: 3 }
        }
    };
    
    const layout = {
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        margin: { l: 20, r: 20, t: 10, b: 20 },
        showlegend: true,
        legend: { orientation: "h", yanchor: "bottom", y: -0.2, xanchor: "center", x: 0.5 },
        annotations: [{
            text: 'ASSETS',
            x: 0.5, y: 0.5,
            font: { size: 20, color: '#FFFFFF' },
            showarrow: false
        }]
    };
    
    Plotly.newPlot('donut-chart', [trace], layout, {responsive: true});
}

// --- NATION OVERVIEW ---

function initNationOverview() {
    const countries = [...new Set(militaryData.map(d => d.country).filter(c => c))].sort();
    
    countries.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        countryList.appendChild(opt);
    });
    
    if (countries.length > 0) {
        countryInput.value = countries[0];
        updateNationOverview();
    }
    
    countryInput.addEventListener('input', () => {
        // Only update if it's a valid country to avoid errors on partial typing
        if (countries.includes(countryInput.value)) {
            updateNationOverview();
        }
    });
}

function updateNationOverview() {
    const selectedCountry = countryInput.value;
    const countryData = militaryData.find(d => d.country === selectedCountry);
    if (!countryData) return;
    
    noPowerIndexEl.textContent = (countryData.power_index || 0).toFixed(4);
    noRankEl.textContent = `Rank: ${Math.floor(countryData.power_index_rank || 0)}`;
    noDefenseBudgetEl.textContent = formatBudget(countryData.defense_budget_usd || 0);
    noActivePersonnelEl.textContent = formatNumber(countryData.active_personnel || 0);
    noTotalAssetsEl.textContent = formatNumber(countryData.total_military_assets || 0);
    
    drawRadarChart(countryData);
    drawHwChart(countryData);
}

function drawRadarChart(countryData) {
    const maxVals = {
        active_personnel: Math.max(...militaryData.map(d => d.active_personnel || 0)),
        tanks: Math.max(...militaryData.map(d => d.tanks || 0)),
        total_military_aircraft: Math.max(...militaryData.map(d => d.total_military_aircraft || 0)),
        total_naval_fleet: Math.max(...militaryData.map(d => d.total_naval_fleet || 0))
    };
    
    const categories = ['Personnel', 'Tanks', 'Aircraft', 'Naval Fleet'];
    const values = [
        maxVals.active_personnel ? (countryData.active_personnel || 0) / maxVals.active_personnel : 0,
        maxVals.tanks ? (countryData.tanks || 0) / maxVals.tanks : 0,
        maxVals.total_military_aircraft ? (countryData.total_military_aircraft || 0) / maxVals.total_military_aircraft : 0,
        maxVals.total_naval_fleet ? (countryData.total_naval_fleet || 0) / maxVals.total_naval_fleet : 0
    ];
    
    // Close the loop
    categories.push(categories[0]);
    values.push(values[0]);
    
    const trace = {
        type: 'scatterpolar',
        r: values,
        theta: categories,
        fill: 'toself',
        fillcolor: 'rgba(255, 0, 127, 0.4)',
        line: { color: '#FF007F', width: 3 },
        marker: { color: '#FFFFFF', size: 8 }
    };
    
    const layout = {
        polar: {
            radialaxis: { visible: true, range: [0, 1], gridcolor: 'rgba(255,255,255,0.1)', linecolor: 'rgba(255,255,255,0.1)' },
            angularaxis: { gridcolor: 'rgba(255,255,255,0.1)', linecolor: 'rgba(255,255,255,0.1)' },
            bgcolor: chartBg
        },
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        margin: { l: 40, r: 40, t: 30, b: 30 }
    };
    
    Plotly.newPlot('radar-chart', [trace], layout, {responsive: true});
}

function drawHwChart(countryData) {
    const types = ['Destroyers', 'Submarines', 'Helicopters', 'Fighters', 'Artillery', 'AFVs', 'Tanks']; // Reversed for Plotly
    const counts = [
        countryData.destroyers || 0,
        countryData.submarines || 0,
        countryData.total_military_helicopters || 0,
        countryData.fighter_aircraft || 0,
        (countryData.self_propelled_artillery || 0) + (countryData.towed_artillery || 0),
        countryData.armored_fighting_vehicles || 0,
        countryData.tanks || 0
    ];
    
    // Custom colors mapping (reversed to match Streamlit's implicit mapping based on the dataframe order)
    // Streamlit mapped discrete colors to types in order. 
    // The Streamlit dataframe order was: Tanks, AFVs, Artillery, Fighters, Helicopters, Submarines, Destroyers
    const cTypes = ['Tanks', 'AFVs', 'Artillery', 'Fighters', 'Helicopters', 'Submarines', 'Destroyers'];
    const colors = types.map(t => customNeonColors[cTypes.indexOf(t) % customNeonColors.length]);
    
    const trace = {
        type: 'bar',
        x: counts,
        y: types,
        orientation: 'h',
        marker: {
            color: colors,
            line: { width: 0 },
            opacity: 0.9
        }
    };
    
    const layout = {
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        margin: { l: 80, r: 20, t: 10, b: 40 },
        xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
        yaxis: { gridcolor: 'rgba(255,255,255,0.1)' }
    };
    
    Plotly.newPlot('hw-bar-chart', [trace], layout, {responsive: true});
}
