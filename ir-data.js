const irDatabase = [
    {
        id: "international-relations",
        title: "International Relations",
        icon: "fas fa-globe-americas",
        progress: 0,
        units: [
            { id: "ir-unit-1", title: "Basics of International Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-2", title: "Evolution of India's Foreign Policy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-3", title: "Events and Developments in Foreign Nations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-4", title: "India and its Neighbourhood Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-5", title: "India and Africa Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-6", title: "India and Central Asia Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-7", title: "India and Europe Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-8", title: "India and Indo-Pacific Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-9", title: "India and South East Asia Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-10", title: "India and West Asia Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-11", title: "India and Latin America-Caribbean Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-12", title: "India and Russia Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-13", title: "India and USA Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-14", title: "Relations with Other Countries", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-15", title: "The United Nations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-16", title: "Multilateral Groupings", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-17", title: "Regional Groupings", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ir-unit-18", title: "Indian Diaspora", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
irDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






