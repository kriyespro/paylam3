const geographyDatabase = [
    {
        id: "indian-geography",
        title: "Indian Geography",
        icon: "fas fa-map-marked-alt",
        progress: 0,
        units: [
            { id: "ig-unit-1", title: "Physical Setting of India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-2", title: "Major Physical Division of India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-3", title: "Drainage System", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-4", title: "Indian Climate", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-5", title: "Indian Monsoon", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-6", title: "Indian Soils", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-7", title: "Land Resource in India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-8", title: "Mineral Resource", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-9", title: "Energy Resources", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-10", title: "Forest", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-11", title: "Agriculture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-12", title: "Manufacturing and Services", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-13", title: "Transport", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-14", title: "Communication", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-15", title: "Hazards and Disasters", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-16", title: "Population and Settlement", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ig-unit-17", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "physical-geography",
        title: "Physical Geography",
        icon: "fas fa-mountain",
        progress: 0,
        units: [
            { id: "pg-unit-1", title: "Universe: Origin and Evolution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-2", title: "Movement of Earth", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-3", title: "Earth's Internal Structure", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-4", title: "Tectonics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-5", title: "Rocks", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-6", title: "Landforms", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-7", title: "Soil", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-8", title: "Atmosphere", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-9", title: "Hydrological Cycle", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-10", title: "Weather Phenomenon", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-11", title: "Ocean", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "pg-unit-12", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "world-geography",
        title: "World Geography",
        icon: "fas fa-globe",
        progress: 0,
        units: [
            { id: "wg-unit-1", title: "Climate Regions of The world", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "wg-unit-2", title: "Oceans", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "wg-unit-3", title: "Continents", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "wg-unit-4", title: "World Economic Geography", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "wg-unit-5", title: "World Human Geography", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "wg-unit-6", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
geographyDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






