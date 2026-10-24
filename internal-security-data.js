const internalSecurityDatabase = [
    {
        id: "internal-security",
        title: "Internal Security",
        icon: "fas fa-shield-alt",
        progress: 0,
        units: [
            { id: "is-unit-1", title: "Internal Security Challenges", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "is-unit-2", title: "Insurgency, Radicalisation and Terrorism", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "is-unit-3", title: "External and Border Threats", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "is-unit-4", title: "Cybercrime and Information Security", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "is-unit-5", title: "Economic and Financial Security", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "is-unit-6", title: "Security Forces and Intelligence", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
internalSecurityDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






