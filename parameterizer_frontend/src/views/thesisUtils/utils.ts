export const createSeries = (index: number, data: number[], seriesName: string = 'Series') => ({
    name: seriesName === 'Series' ? `${seriesName} ${index + 1}` : seriesName,
    data,
    lineWidth: 1.25,
    pointStart: Date.UTC(2010, 1, 1),
    pointInterval: 1000 * 60 * 30, // Granularity of 30 minutes
    // This will return false if index is even, and true if it's odd
    // If larger than 10, it will return true every 10th index
    visible: index < 10 ? index % 2 !==1 : index % 10 === 0,
    tooltip: {
        valueDecimals: 2
    },
    plotOptions: {
        series: {
            showInNavigator: index < 10 ? index % 2 !== 0 : index % 10 === 0,
        }
    }
});

// Utility function to segment your data based on the presence of null in the referenceData array
const createSegments = (data: number[], referenceData: number[]) => {
  const segments = [];
  let currentSegment = [];
  let currentWidth = referenceData[0] === null ? 2.5 : 1;  // Adjust widths as necessary

  for (let i = 0; i < data.length; i++) {
    if (referenceData[i] === null && currentWidth === 1) {
      if (currentSegment.length) {
        segments.push({data: currentSegment, lineWidth: 1.25});
        currentSegment = [];
      }
      currentWidth = 2.5;
    } else if (referenceData[i] !== null && currentWidth === 2.5) {
      if (currentSegment.length) {
        segments.push({data: currentSegment, lineWidth: 2.5});
        currentSegment = [];
      }
      currentWidth = 1.25;
    }
    currentSegment.push(data[i]);
  }
  if (currentSegment.length) {
    segments.push({data: currentSegment, lineWidth: currentWidth});
  }

  return segments;
};

export const createSegmentedSeries = (index: number, data: number[], referenceData: number[], seriesName: string = 'Series') => {
    console.log(data)
    console.log(referenceData)
    const segments = createSegments(data, referenceData);
    console.log("Segments:", segments);

    return segments.map(segment => ({
        name: seriesName === 'Series' ? `${seriesName} ${index + 1}` : seriesName,
        data: segment.data,
        lineWidth: segment.lineWidth,
        pointStart: Date.UTC(2010, 1, 1),
        pointInterval: 1000 * 60 * 30, // Granularity of 30 minutes
        visible: index < 10 ? index % 2 !== 1 : index % 10 === 0,
        tooltip: {
            valueDecimals: 2
        },
        plotOptions: {
            series: {
                showInNavigator: index < 10 ? index % 2 !== 0 : index % 10 === 0,
            }
        }
    }));
};

export const generateChartOptions = (title, seriesName) => ({
    credits: {
        enabled: false
    },
    title: {
        text: title
    },
    navigator: {
        enabled: true
    },
    legend: {
        title: {
            text: '<span style="font-size: 11px; color: #666; font-weight: normal;">(Click on series to hide)</span>',
            style: {
                fontStyle: 'italic'
            }
        },
        verticalAlign: "top"
    },
    xAxis: {
        type: 'datetime'
    },
    colors: [
        '#058DC7',  // Blue
        '#50B432',  // Green
        '#ED561B',  // Orange-Red
        '#DDDF00',  // Yellow
        '#24CBE5',  // Light Blue
        '#64E572',  // Light Green
        '#FF9655',  // Light Orange
        '#FFD700',  // Gold
        '#6AF9C4',  // Aqua
        '#FF69B4',  // Pink
        '#A020F0',  // Purple
        '#8B4513',  // Saddle Brown
        '#2E8B57',  // Sea Green
        '#D2691E',  // Chocolate
        '#B22222',  // Firebrick
        '#20B2AA',  // Light Sea Green
        '#8A2BE2',  // BlueViolet
        '#5F9EA0',  // CadetBlue
        '#FFF263',  // Pale Yellow
        '#7B68EE'   // MediumSlateBlue
    ],
    chart: {
        height: 700,
        type: 'line',
        zoomType: 'x',
        panning: true,
        panKey: 'shift'
    },
    rangeSelector: {
        selected: 1,
        x: 0,
        // floating: true,
        style: {
            color: 'black',
            fontWeight: 'bold',
            position: 'relative',
            "font-family": "Arial"
        },
        enabled: true,
        inputEnabled: false,
        // inputDateFormat: '%y',
        // inputEditDateFormat: '%y',
        buttons: [
            {
                type: 'hour',
                count: 12,
                text: '12H'
            },
            {
                type: 'day',
                count: 3,
                text: '3D'
            },

            {
                type: 'day',
                count: 5,
                text: '5D'
            },
            {
                type: 'week',
                count: 1,
                text: 'W'
            },
            {
                type: 'month',
                count: 1,
                text: 'M'
            },

            {
                type: 'all',
                text: 'All',
                align: 'right',
                x: 1000,
                y: 100,
            }],
    },
    series: [{
        name: seriesName,
        data: Uint32Array.from({length: 10000}, () => Math.floor(Math.random() * 0)),
        pointStart: Date.UTC(2010, 1, 1),
        pointInterval: 1000 * 60 * 30, // Granularity of 30 minutes
        tooltip: {
            valueDecimals: 2
        }
    }],
    // plotOptions: {
    //   series: {
    //     pointStart: Date.UTC(2010, 0, 1),
    //     pointInterval: 100000 * 1000 // one day
    //   }
    // },
});

export const generateChartOptionsLarge = (title, seriesName) => ({
    credits: {
        enabled: false
    },
    title: {
        text: title
    },
    navigator: {
        enabled: true
    },
    legend: {
        title: {
            text: '<span style="font-size: 11px; color: #666; font-weight: normal;">(Click on series to hide)</span>',
            style: {
                fontStyle: 'italic'
            }
        },
        verticalAlign: "top"
    },
    xAxis: {
        type: 'datetime'
    },
    chart: {
        height: 810,
        type: 'line',
        zoomType: 'x',
        panning: true,
        panKey: 'shift'
    },
    colors: [
        '#058DC7',  // Blue
        '#50B432',  // Green
        '#ED561B',  // Orange-Red
        '#DDDF00',  // Yellow
        '#24CBE5',  // Light Blue
        '#64E572',  // Light Green
        '#FF9655',  // Light Orange
        '#FFD700',  // Gold
        '#6AF9C4',  // Aqua
        '#FF69B4',  // Pink
        '#A020F0',  // Purple
        '#8B4513',  // Saddle Brown
        '#2E8B57',  // Sea Green
        '#D2691E',  // Chocolate
        '#B22222',  // Firebrick
        '#20B2AA',  // Light Sea Green
        '#8A2BE2',  // BlueViolet
        '#5F9EA0',  // CadetBlue
        '#FFF263',  // Pale Yellow
        '#7B68EE'   // MediumSlateBlue
    ],
    rangeSelector: {
        selected: 1,
        x: 0,
        // floating: true,
        style: {
            color: 'black',
            fontWeight: 'bold',
            position: 'relative',
            "font-family": "Arial"
        },
        enabled: true,
        inputEnabled: false,
        // inputDateFormat: '%y',
        // inputEditDateFormat: '%y',
        buttons: [
            {
                type: 'hour',
                count: 12,
                text: '12H'
            },
            {
                type: 'day',
                count: 3,
                text: '3D'
            },

            {
                type: 'day',
                count: 5,
                text: '5D'
            },
            {
                type: 'week',
                count: 1,
                text: 'W'
            },
            {
                type: 'month',
                count: 1,
                text: 'M'
            },

            {
                type: 'all',
                text: 'All',
                align: 'right',
                x: 900,
                y: 100,
            }],
    },
    plotOptions: {
        series: {
            showInNavigator: true
        }
    },
    series: [{
        name: seriesName,
        data: Uint32Array.from({length: 10000}, () => Math.floor(Math.random() * 0)),
        pointStart: Date.UTC(2010, 1, 1),
        pointInterval: 1000 * 60 * 30, // Granularity of 30 minutes
        tooltip: {
            valueDecimals: 2
        }
    }],
});