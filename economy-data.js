const economyDatabase = [
    {
        id: "economy",
        title: "Economics",
        icon: "fas fa-chart-line",
        progress: 0,
        units: [
            { id: "eco-unit-1", title: "Introduction to Economics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-2", title: "National Income Accounting", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-3", title: "Money, Banking and Monetary Policy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-4", title: "Finance and Financial Markets", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-5", title: "Public Finance in India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-6", title: "Taxation in India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-7", title: "Inflation", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-8", title: "Unemployment", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-9", title: "Poverty", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-10", title: "Agriculture and Allied Activities", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-11", title: "Food Processing", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-12", title: "Industry and Manufacturing", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-13", title: "Infrastructure and Investment Models in India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-14", title: "Services and Digital Economy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-15", title: "Trade and External Sector", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-16", title: "Planning and Reform", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-17", title: "International Institutions", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "eco-unit-18", title: "Sustainable and Inclusive Growth", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "final-revision-section",
        title: "Final Revision",
        icon: "fas fa-check-double",
        progress: 0,
        units: [
            { id: "final-rev-1", title: "Complete units Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "final-rev-2", title: "Mock Tests & Practice", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    }
];

// Utility function to calculate overall progress of a subject based on completed lessons
function calculateProgress(subject) {
    let totalLessons = 0;
    let completedLessons = 0;

    subject.units.forEach(unit => {
        totalLessons += unit.lessons.length;
        completedLessons += unit.lessons.filter(l => l.completed).length;
    });

    if (totalLessons === 0) return 0;
    return Math.round((completedLessons / totalLessons) * 100);
}

// Pre-calculate progress for all subjects on load
economyDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});








