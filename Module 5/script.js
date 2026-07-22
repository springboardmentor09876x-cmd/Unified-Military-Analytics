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
const allianceFilter = document.getElementById('alliance-filter');
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

    // Populate Alliances
    const alliances = [...new Set(militaryData.map(d => String(d.alliance)).filter(a => a !== 'nan' && a !== ''))].sort();
    allianceFilter.innerHTML = '<option value="All">All</option>';
    alliances.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a;
        opt.textContent = a;
        allianceFilter.appendChild(opt);
    });

    continentFilter.addEventListener('change', () => {
        updateRegionFilter();
        updateQuickStats();
    });
    
    regionFilter.addEventListener('change', updateQuickStats);
    allianceFilter.addEventListener('change', updateQuickStats);

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
    const selectedAlliance = allianceFilter.value;
    
    let filtered = militaryData;
    if (selectedContinent !== 'All') {
        filtered = filtered.filter(d => d.continent === selectedContinent);
    }
    if (selectedRegion !== 'All') {
        filtered = filtered.filter(d => d.region === selectedRegion);
    }
    if (selectedAlliance !== 'All') {
        filtered = filtered.filter(d => d.alliance === selectedAlliance);
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
}

function drawTop10Chart(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('bar-chart');
        return;
    }
    
    // Top 10 by Power Index
    // Note: lower is better, but we need to sort ascending first.
    let validCountries = filtered.filter(d => d.power_index > 0);
    let sorted = [...validCountries].sort((a, b) => a.power_index - b.power_index);
    let top10 = sorted.slice(0, 10).reverse(); // Reverse for plotly horizontal bar
    
    const trace = {
        x: top10.map(d => d.power_index),
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
        },
        hovertemplate: '<b>%{y}</b><br>Power Index: %{x:.4f}<extra></extra>'
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
    const rawValues = [
        countryData.active_personnel || 0,
        countryData.tanks || 0,
        countryData.total_military_aircraft || 0,
        countryData.total_naval_fleet || 0
    ];
    
    const maxValuesList = [
        maxVals.active_personnel,
        maxVals.tanks,
        maxVals.total_military_aircraft,
        maxVals.total_naval_fleet
    ];
    
    const values = rawValues.map((v, i) => maxValuesList[i] ? v / maxValuesList[i] : 0);
    const hoverTexts = rawValues.map((v, i) => `${formatNumber(v)}<br>Global Max: ${formatNumber(maxValuesList[i])}`);
    
    // Close the loop
    categories.push(categories[0]);
    values.push(values[0]);
    hoverTexts.push(hoverTexts[0]);
    
    const trace = {
        type: 'scatterpolar',
        r: values,
        theta: categories,
        text: hoverTexts,
        hovertemplate: '<b>%{theta}</b><br>%{text}<extra></extra>',
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
    
    // Calculate max values for comparisons
    const maxVals = {
        'Destroyers': Math.max(...militaryData.map(d => d.destroyers || 0)),
        'Submarines': Math.max(...militaryData.map(d => d.submarines || 0)),
        'Helicopters': Math.max(...militaryData.map(d => d.total_military_helicopters || 0)),
        'Fighters': Math.max(...militaryData.map(d => d.fighter_aircraft || 0)),
        'Artillery': Math.max(...militaryData.map(d => (d.self_propelled_artillery || 0) + (d.towed_artillery || 0))),
        'AFVs': Math.max(...militaryData.map(d => d.armored_fighting_vehicles || 0)),
        'Tanks': Math.max(...militaryData.map(d => d.tanks || 0))
    };
    
    const counts = [
        countryData.destroyers || 0,
        countryData.submarines || 0,
        countryData.total_military_helicopters || 0,
        countryData.fighter_aircraft || 0,
        (countryData.self_propelled_artillery || 0) + (countryData.towed_artillery || 0),
        countryData.armored_fighting_vehicles || 0,
        countryData.tanks || 0
    ];
    
    const hoverTexts = types.map((t, i) => `${formatNumber(counts[i])}<br>Global Max: ${formatNumber(maxVals[t])}`);
    
    // Custom colors mapping
    const cTypes = ['Tanks', 'AFVs', 'Artillery', 'Fighters', 'Helicopters', 'Submarines', 'Destroyers'];
    const colors = types.map(t => customNeonColors[cTypes.indexOf(t) % customNeonColors.length]);
    
    const trace = {
        type: 'bar',
        x: counts,
        y: types,
        text: hoverTexts,
        hovertemplate: '<b>%{y}</b><br>Count: %{text}<extra></extra>',
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
