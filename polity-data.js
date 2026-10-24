const polityDatabase = [
    {
        id: "polity",
        title: "Indian Polity",
        icon: "fas fa-gavel",
        progress: 0,
        units: [
            { id: "p-unit-1", title: "Historical Background", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-2", title: "Concept and Salient Features of the Constitution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-3", title: "Preamble of the Constitution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-4", title: "Union and Its Territory", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-5", title: "Citizenship", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-6", title: "Fundamental Rights", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-7", title: "Directive Principles of State Policy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-8", title: "Fundamental Duties", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-9", title: "Union Executive", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-10", title: "Parliament", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-11", title: "Parliamentary Committees", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-12", title: "State Executive", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-13", title: "State Legislature", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-14", title: "Union Territories and Special Areas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-15", title: "Supreme Court", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-16", title: "High Court", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-17", title: "Subordinate Courts", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-18", title: "Alternative Dispute Resolution Courts", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-19", title: "Tribunals", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-20", title: "Judicial Review", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-21", title: "Basic Structure", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-22", title: "Basics of Federal System", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-23", title: "Centre-State Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-24", title: "Inter-State Relations", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-25", title: "Panchayati Raj", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-26", title: "Urban Local Bodies", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-27", title: "Elections", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-28", title: "Political Dynamics", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-29", title: "Emergency Provisions", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-30", title: "Amendment of the Constitution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-31", title: "Other Constitutional Dimensions", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-32", title: "Constitutional Bodies", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-33", title: "Non-Constitutional Bodies", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-34", title: "Constituents of Indian Constitution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "p-unit-35", title: "Laws and Legislations", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
polityDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






