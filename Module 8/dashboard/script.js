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



// Compare Powers DOM
const comparePowersSection = document.getElementById('compare-powers');
const cp1Input = document.getElementById('compare-1-input');
const cp2Input = document.getElementById('compare-2-input');
const cp1Name = document.getElementById('cp1-name');
const cp2Name = document.getElementById('cp2-name');
const cp1Pi = document.getElementById('cp1-pi');
const cp2Pi = document.getElementById('cp2-pi');
const cp1Budget = document.getElementById('cp1-budget');
const cp2Budget = document.getElementById('cp2-budget');
const cp1Stats = document.getElementById('cp1-stats');
const cp2Stats = document.getElementById('cp2-stats');

// Coalition Builder DOM
const coalitionBuilderSection = document.getElementById('coalition-builder');
const coalitionSearch = document.getElementById('coalition-search');
const coalitionTagsContainer = document.getElementById('coalition-tags');
const coalitionDropdown = document.getElementById('coalition-dropdown');
const adversaryInput = document.getElementById('adversary-input');
const coalitionBudgetEl = document.getElementById('coalition-budget');
const coalitionManpowerEl = document.getElementById('coalition-manpower');
const adversaryNameLabel = document.getElementById('adversary-name-label');
const adversaryBudgetEl = document.getElementById('adversary-budget');
const adversaryManpowerEl = document.getElementById('adversary-manpower');

let selectedCoalition = [];

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
    initComparePowers();
    initCoalitionBuilder();
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
            quickStatsSection.classList.remove('active');
            nationOverviewSection.classList.remove('active');
            comparePowersSection.classList.remove('active');
            coalitionBuilderSection.classList.remove('active');

            if (e.target.value === 'Quick Stats') {
                quickStatsSection.classList.add('active');
            } else if (e.target.value === 'Nation Overview') {
                nationOverviewSection.classList.add('active');
            } else if (e.target.value === 'Compare Powers') {
                comparePowersSection.classList.add('active');
            } else if (e.target.value === 'Coalition Builder') {
                coalitionBuilderSection.classList.add('active');
            }
            window.dispatchEvent(new Event('resize'));
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
    drawKPIChart(filtered);
    drawDonutCharts(filtered);
    drawWorldMap(filtered);
}

function drawKPIChart(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('kpi-budget-gdp');
        return;
    }
    
    // Average Budget to GDP Ratio
    const avgRatio = filtered.reduce((sum, d) => sum + (d.budget_to_gdp_ratio || 0), 0) / filtered.length;
    const percentage = avgRatio * 100;
    
    const data = [
        {
            type: "indicator",
            mode: "gauge+number",
            value: percentage,
            number: { suffix: "%", valueformat: ".2f", font: { color: "#FFFFFF" } },
            title: { text: "Avg Budget to GDP", font: { color: "#FFFFFF" } },
            gauge: {
                axis: { range: [null, 15], tickwidth: 1, tickcolor: "rgba(255,255,255,0.5)" },
                bar: { color: "#00F0FF" },
                bgcolor: "rgba(255,255,255,0.1)",
                borderwidth: 2,
                bordercolor: "transparent",
                steps: [
                    { range: [0, 2], color: "rgba(57, 255, 20, 0.3)" },
                    { range: [2, 5], color: "rgba(255, 214, 10, 0.3)" },
                    { range: [5, 15], color: "rgba(255, 0, 127, 0.3)" }
                ]
            }
        }
    ];

    const layout = {
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        margin: { l: 20, r: 20, t: 40, b: 20 },
        font: { color: '#FFFFFF' }
    };
    
    Plotly.newPlot('kpi-budget-gdp', data, layout, {responsive: true});
}

function drawDonutCharts(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('donut-ppp');
        Plotly.purge('donut-assets');
        Plotly.purge('donut-naval');
        Plotly.purge('donut-air');
        Plotly.purge('donut-land');
        Plotly.purge('donut-budget');
        return;
    }

    const createDonutData = (sortField, isSumFunction = null) => {
        let sorted = [...filtered].sort((a, b) => {
            const valA = isSumFunction ? isSumFunction(a) : (a[sortField] || 0);
            const valB = isSumFunction ? isSumFunction(b) : (b[sortField] || 0);
            return valB - valA;
        });
        
        const top5 = sorted.slice(0, 5);
        const values = top5.map(d => isSumFunction ? isSumFunction(d) : (d[sortField] || 0));
        const labels = top5.map(d => d.country);
        
        return {
            values: values,
            labels: labels,
            type: 'pie',
            hole: .4,
            textinfo: 'label+percent',
            textposition: 'inside',
            marker: {
                colors: customNeonColors
            },
            hoverinfo: 'label+value'
        };
    };

    const layout = {
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        showlegend: false,
        margin: { l: 20, r: 20, t: 20, b: 20 },
        font: { color: '#FFFFFF' }
    };

    // 1. PPP
    Plotly.newPlot('donut-ppp', [createDonutData('purchasing_power_parity_usd')], layout, {responsive: true});
    
    // 2. Military Assets
    Plotly.newPlot('donut-assets', [createDonutData('total_military_assets')], layout, {responsive: true});
    
    // 3. Naval Fleet
    Plotly.newPlot('donut-naval', [createDonutData('total_naval_fleet')], layout, {responsive: true});
    
    // 4. Air Fleet
    Plotly.newPlot('donut-air', [createDonutData('total_military_aircraft')], layout, {responsive: true});
    
    // 5. Land Fleet (Sum of land vehicles)
    const getLandFleet = d => (d.tanks || 0) + (d.armored_fighting_vehicles || 0) + (d.self_propelled_artillery || 0) + (d.towed_artillery || 0) + (d.rocket_projectors || 0);
    Plotly.newPlot('donut-land', [createDonutData(null, getLandFleet)], layout, {responsive: true});
    
    // 6. Defense Budget
    Plotly.newPlot('donut-budget', [createDonutData('defense_budget_usd')], layout, {responsive: true});
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

// --- WORLD MAP ---
function drawWorldMap(filtered) {
    if (filtered.length === 0) {
        Plotly.purge('world-map');
        return;
    }

    const z = filtered.map(d => d.power_index || 0.0);
    const text = filtered.map(d => `${d.country}<br>PI: ${(d.power_index||0).toFixed(4)}`);

    const data = [{
        type: 'choropleth',
        locationmode: 'country names',
        locations: filtered.map(d => d.country),
        z: z,
        text: text,
        colorscale: [
            [0, '#39FF14'], [0.2, '#00F0FF'], [0.5, '#FFD60A'], [1, '#FF007F']
        ],
        reversescale: true,
        marker: {
            line: {
                color: 'rgba(255,255,255,0.1)',
                width: 1
            }
        },
        colorbar: {
            title: 'Power Index',
            tickfont: { color: '#FFF' },
            titlefont: { color: '#FFF' }
        }
    }];

    const layout = {
        geo: {
            showframe: false,
            showcoastlines: true,
            coastlinecolor: 'rgba(255,255,255,0.2)',
            projection: { type: 'equirectangular' },
            bgcolor: 'transparent',
            showland: true,
            landcolor: '#1A1A24',
            showocean: true,
            oceancolor: '#0D0E15'
        },
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        margin: { l: 0, r: 0, t: 0, b: 0 }
    };

    let mapConfig = { responsive: true, scrollZoom: false };
    Plotly.newPlot('world-map', data, layout, mapConfig);

    const mapDiv = document.getElementById('world-map');
    
    mapDiv.addEventListener('mousedown', function() {
        if (!mapConfig.scrollZoom) {
            mapConfig.scrollZoom = true;
            Plotly.react('world-map', data, layout, mapConfig);
        }
    });

    mapDiv.addEventListener('mouseleave', function() {
        if (mapConfig.scrollZoom) {
            mapConfig.scrollZoom = false;
            Plotly.react('world-map', data, layout, mapConfig);
        }
    });
}

// --- COMPARE POWERS ---
function initComparePowers() {
    const countries = [...new Set(militaryData.map(d => d.country).filter(c => c))].sort();
    
    if (countries.length >= 2) {
        cp1Input.value = countries[0];
        cp2Input.value = countries[1];
        updateComparePowers();
    }

    cp1Input.addEventListener('input', () => {
        if (countries.includes(cp1Input.value)) updateComparePowers();
    });
    cp2Input.addEventListener('input', () => {
        if (countries.includes(cp2Input.value)) updateComparePowers();
    });
}

function updateComparePowers() {
    const c1Name = cp1Input.value;
    const c2Name = cp2Input.value;
    const c1Data = militaryData.find(d => d.country === c1Name);
    const c2Data = militaryData.find(d => d.country === c2Name);

    if (c1Data) {
        cp1Name.textContent = c1Data.country;
        cp1Pi.textContent = `PI: ${(c1Data.power_index || 0).toFixed(4)}`;
        cp1Budget.textContent = `Budget: ${formatBudget(c1Data.defense_budget_usd || 0)}`;
        cp1Stats.textContent = `${formatNumber(c1Data.total_military_manpower || 0)} / ${formatNumber(c1Data.total_military_aircraft || 0)} / ${formatNumber(c1Data.total_naval_fleet || 0)}`;
    }
    
    if (c2Data) {
        cp2Name.textContent = c2Data.country;
        cp2Pi.textContent = `PI: ${(c2Data.power_index || 0).toFixed(4)}`;
        cp2Budget.textContent = `Budget: ${formatBudget(c2Data.defense_budget_usd || 0)}`;
        cp2Stats.textContent = `${formatNumber(c2Data.total_military_manpower || 0)} / ${formatNumber(c2Data.total_military_aircraft || 0)} / ${formatNumber(c2Data.total_naval_fleet || 0)}`;
    }

    if (c1Data && c2Data) {
        drawCompareRadar(c1Data, c2Data);
        drawCompareBar(c1Data, c2Data);
    }
}

function drawCompareRadar(c1, c2) {
    const maxVals = {
        manpower: Math.max(...militaryData.map(d => d.total_military_manpower || 0)),
        aircraft: Math.max(...militaryData.map(d => d.total_military_aircraft || 0)),
        navy: Math.max(...militaryData.map(d => d.total_naval_fleet || 0)),
        tanks: Math.max(...militaryData.map(d => d.tanks || 0))
    };

    const categories = ['Manpower', 'Aircraft', 'Navy', 'Tanks'];
    
    const getNormalized = (c) => [
        (c.total_military_manpower || 0) / maxVals.manpower,
        (c.total_military_aircraft || 0) / maxVals.aircraft,
        (c.total_naval_fleet || 0) / maxVals.navy,
        (c.tanks || 0) / maxVals.tanks
    ];

    const getRaw = (c) => [
        c.total_military_manpower || 0,
        c.total_military_aircraft || 0,
        c.total_naval_fleet || 0,
        c.tanks || 0
    ];

    const r1 = getNormalized(c1); r1.push(r1[0]);
    const r2 = getNormalized(c2); r2.push(r2[0]);
    
    let cats = [...categories]; cats.push(cats[0]);

    const raw1 = getRaw(c1); raw1.push(raw1[0]);
    const raw2 = getRaw(c2); raw2.push(raw2[0]);

    const trace1 = {
        type: 'scatterpolar',
        r: r1,
        theta: cats,
        fill: 'toself',
        name: c1.country,
        line: {color: '#00F0FF'},
        text: raw1.map(v => formatNumber(v)),
        hovertemplate: '%{theta}: %{text}<extra></extra>'
    };

    const trace2 = {
        type: 'scatterpolar',
        r: r2,
        theta: cats,
        fill: 'toself',
        name: c2.country,
        line: {color: '#FF007F'},
        text: raw2.map(v => formatNumber(v)),
        hovertemplate: '%{theta}: %{text}<extra></extra>'
    };

    const layout = {
        polar: {
            radialaxis: { visible: true, range: [0, 1], gridcolor: 'rgba(255,255,255,0.1)' },
            angularaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
            bgcolor: chartBg
        },
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        margin: { l: 40, r: 40, t: 30, b: 30 },
        showlegend: true,
        legend: { font: { color: '#FFF' }, orientation: 'h', y: -0.2 }
    };

    Plotly.newPlot('compare-radar-chart', [trace1, trace2], layout, {responsive: true});
}

function drawCompareBar(c1, c2) {
    const categories = ['Budget ($)', 'Manpower', 'Aircraft', 'Navy', 'Tanks'];
    
    const v1 = [
        c1.defense_budget_usd || 0,
        c1.total_military_manpower || 0,
        c1.total_military_aircraft || 0,
        c1.total_naval_fleet || 0,
        c1.tanks || 0
    ];
    const v2 = [
        c2.defense_budget_usd || 0,
        c2.total_military_manpower || 0,
        c2.total_military_aircraft || 0,
        c2.total_naval_fleet || 0,
        c2.tanks || 0
    ];

    const trace1 = {
        x: categories,
        y: v1,
        name: c1.country,
        type: 'bar',
        marker: { color: '#00F0FF' }
    };
    
    const trace2 = {
        x: categories,
        y: v2,
        name: c2.country,
        type: 'bar',
        marker: { color: '#FF007F' }
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        yaxis: { type: 'log', gridcolor: 'rgba(255,255,255,0.1)' },
        xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
        margin: { l: 60, r: 20, t: 30, b: 40 },
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    };

    Plotly.newPlot('compare-bar-chart', [trace1, trace2], layout, {responsive: true});
}

// --- COALITION BUILDER ---
function initCoalitionBuilder() {
    const countries = [...new Set(militaryData.map(d => d.country).filter(c => c))].sort();
    
    if (countries.length > 0) {
        adversaryInput.value = countries.includes('Russia') ? 'Russia' : countries[0];
        updateCoalitionView();
    }

    adversaryInput.addEventListener('input', () => {
        if (countries.includes(adversaryInput.value)) updateCoalitionView();
    });

    coalitionSearch.addEventListener('input', (e) => {
        const val = e.target.value.toLowerCase();
        coalitionDropdown.innerHTML = '';
        if (val) {
            const matches = countries.filter(c => c.toLowerCase().includes(val) && !selectedCoalition.includes(c));
            if (matches.length > 0) {
                coalitionDropdown.classList.remove('hidden');
                matches.slice(0, 10).forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'dropdown-item';
                    div.textContent = c;
                    div.onclick = () => {
                        addCountryToCoalition(c);
                        coalitionSearch.value = '';
                        coalitionDropdown.classList.add('hidden');
                    };
                    coalitionDropdown.appendChild(div);
                });
            } else {
                coalitionDropdown.classList.add('hidden');
            }
        } else {
            coalitionDropdown.classList.add('hidden');
        }
    });

    if (countries.includes('United States') && countries.includes('United Kingdom')) {
        addCountryToCoalition('United States');
        addCountryToCoalition('United Kingdom');
    }
}

function addCountryToCoalition(country) {
    if (!selectedCoalition.includes(country)) {
        selectedCoalition.push(country);
        renderCoalitionTags();
        updateCoalitionView();
    }
}

function removeCountryFromCoalition(country) {
    selectedCoalition = selectedCoalition.filter(c => c !== country);
    renderCoalitionTags();
    updateCoalitionView();
}

function renderCoalitionTags() {
    coalitionTagsContainer.innerHTML = '';
    selectedCoalition.forEach(c => {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `<span>${c}</span> <span class="remove-tag">×</span>`;
        tag.querySelector('.remove-tag').onclick = () => removeCountryFromCoalition(c);
        coalitionTagsContainer.appendChild(tag);
    });
}

function updateCoalitionView() {
    const adversaryName = adversaryInput.value;
    const adversaryData = militaryData.find(d => d.country === adversaryName);

    const coalitionData = militaryData.filter(d => selectedCoalition.includes(d.country));

    let coalBudget = 0, coalManpower = 0, coalAircraft = 0, coalNavy = 0, coalTanks = 0;
    coalitionData.forEach(d => {
        coalBudget += d.defense_budget_usd || 0;
        coalManpower += d.total_military_manpower || 0;
        coalAircraft += d.total_military_aircraft || 0;
        coalNavy += d.total_naval_fleet || 0;
        coalTanks += d.tanks || 0;
    });

    coalitionBudgetEl.textContent = formatBudget(coalBudget);
    coalitionManpowerEl.textContent = formatNumber(coalManpower);

    let advBudget = 0, advManpower = 0, advAircraft = 0, advNavy = 0, advTanks = 0;
    if (adversaryData) {
        adversaryNameLabel.textContent = adversaryData.country + ' Budget';
        advBudget = adversaryData.defense_budget_usd || 0;
        advManpower = adversaryData.total_military_manpower || 0;
        advAircraft = adversaryData.total_military_aircraft || 0;
        advNavy = adversaryData.total_naval_fleet || 0;
        advTanks = adversaryData.tanks || 0;
        adversaryBudgetEl.textContent = formatBudget(advBudget);
        adversaryManpowerEl.textContent = formatNumber(advManpower);
    }

    drawCoalitionBarChart(
        {budget: coalBudget, manpower: coalManpower, aircraft: coalAircraft, navy: coalNavy, tanks: coalTanks},
        {budget: advBudget, manpower: advManpower, aircraft: advAircraft, navy: advNavy, tanks: advTanks},
        adversaryName || 'Adversary'
    );
}

function drawCoalitionBarChart(coalition, adversary, advName) {
    const categories = ['Budget ($)', 'Manpower', 'Aircraft', 'Navy', 'Tanks'];
    
    const v1 = [coalition.budget, coalition.manpower, coalition.aircraft, coalition.navy, coalition.tanks];
    const v2 = [adversary.budget, adversary.manpower, adversary.aircraft, adversary.navy, adversary.tanks];

    const trace1 = {
        x: categories,
        y: v1,
        name: 'Coalition',
        type: 'bar',
        marker: { color: '#39FF14' }
    };
    
    const trace2 = {
        x: categories,
        y: v2,
        name: advName,
        type: 'bar',
        marker: { color: '#FF5733' }
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: chartBg,
        plot_bgcolor: chartBg,
        font: { color: '#FFFFFF' },
        yaxis: { type: 'log', gridcolor: 'rgba(255,255,255,0.1)' },
        xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
        margin: { l: 60, r: 20, t: 30, b: 40 },
        showlegend: true,
        legend: { orientation: 'h', y: 1.1 }
    };

    Plotly.newPlot('coalition-bar-chart', [trace1, trace2], layout, {responsive: true});
}
