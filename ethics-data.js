const ethicsDatabase = [
    {
        id: "ethics",
        title: "Ethics",
        icon: "fas fa-brain",
        progress: 0,
        units: [
            { id: "et-unit-1", title: "Introduction to Ethics and Moral Philosophy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-2", title: "Ethics and Human Interface", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-3", title: "Human Values and Socialisation", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-4", title: "Attitude and Behaviour", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-5", title: "Emotional Intelligence", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-6", title: "Foundational Values for Civil Services", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-7", title: "Aptitude and Civil Service Ethics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-8", title: "Ethics in Public Administration and Governance", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-9", title: "Probity in Governance", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-10", title: "Corporate and Economic Ethics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-11", title: "Thinkers and Philosophical Foundations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "et-unit-12", title: "Case Studies and Ethical Application Frameworks", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
ethicsDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






