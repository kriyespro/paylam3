const environmentDatabase = [
    {
        id: "environment",
        title: "Environment & Ecology",
        icon: "fas fa-leaf",
        progress: 0,
        units: [
            { id: "e-unit-1", title: "Ecology", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-2", title: "Functions of Ecosystem", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-3", title: "Terrestrial Ecosystem", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-4", title: "Aquatic Ecosystem", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-5", title: "Wet Land Ecosystem", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-6", title: "Environmental Pollution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-7", title: "Renewable Energy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-8", title: "Environmental Impact Assessment (EIA)", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-9", title: "Biodiversity Basics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-10", title: "Indian Biodiversity â€“ Diverse Landscape", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-11", title: "Schedule Animals of WPA 1972", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-12", title: "Animal Diversity of India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-13", title: "Plant Diversity of India", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-14", title: "Marine Organisms", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-15", title: "Protected Area Network", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-16", title: "Conservation Efforts", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-17", title: "Climate Change", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-18", title: "Ocean Acidification", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-19", title: "Ozone Depletion", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-20", title: "Impact of Climate Change", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "e-unit-21", title: "Mitigation Strategies", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
environmentDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






