// DOM Labeler
let labels = [];

function unmarkPage() {
    for (const label of labels) {
        document.body.removeChild(label);
    }
    labels = [];
}

function markPage() {
    unmarkPage();

    var bodyRect = document.body.getBoundingClientRect();
    var items = Array.prototype.slice.call(document.querySelectorAll('*'))
        .map(function (element) {
            var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
            var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

            var rects = [...element.getClientRects()].filter(bb => {
                var center_x = bb.left + bb.width / 2;
                var center_y = bb.top + bb.height / 2;
                var elAtCenter = document.elementFromPoint(center_x, center_y);

                return elAtCenter === element || element.contains(elAtCenter);
            }).map(bb => {
                const rect = {
                    left: Math.max(0, bb.left - bodyRect.left),
                    top: Math.max(0, bb.top - bodyRect.top),
                    right: Math.min(vw, bb.right - bodyRect.left),
                    bottom: Math.min(vh, bb.bottom - bodyRect.top)
                };
                return {
                    ...rect,
                    width: rect.right - rect.left,
                    height: rect.bottom - rect.top
                };
            });

            var area = rects.reduce((acc, rect) => acc + rect.width * rect.height, 0);

            return {
                element: element,
                include: (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") ||
                    (element.tagName === "BUTTON" || element.tagName === "A" || (element.onclick != null) || window.getComputedStyle(element).cursor === "pointer") ||
                    (element.tagName === "IFRAME" || element.tagName === "VIDEO"),
                area,
                rects,
                text: element.textContent.trim().replace(/\s{2,}/g, ' ')
            };
        }).filter(item =>
            item.include && (item.area >= 20)
        );

    // Only keep inner clickable items
    items = items.filter(x => !items.some(y => x.element.contains(y.element) && !(x === y)));

    // Function to generate random colors
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // COCO-like annotations array
    let annotations = [];

    // Let's create a floating border on top of these elements that will always be visible
    items.forEach(function (item, index) {
        item.rects.forEach((bbox) => {
            // Create visual markers
            var newElement = document.createElement("div");
            var borderColor = getRandomColor();
            newElement.style.outline = `2px dashed ${borderColor}`;
            newElement.style.position = "absolute";
            newElement.style.left = `${bbox.left}px`;
            newElement.style.top = `${bbox.top}px`;
            newElement.style.width = `${bbox.width}px`;
            newElement.style.height = `${bbox.height}px`;
            newElement.style.pointerEvents = "none";
            newElement.style.boxSizing = "border-box";
            newElement.style.zIndex = "2147483647";

            // Add floating label at the corner
            var label = document.createElement("span");
            label.textContent = index;
            label.style.position = "absolute";
            label.style.top = "-19px";
            label.style.left = "0px";
            label.style.background = borderColor;
            label.style.color = "white";
            label.style.padding = "2px 4px";
            label.style.fontSize = "12px";
            label.style.borderRadius = "2px";

            newElement.appendChild(label);
            document.body.appendChild(newElement);
            labels.push(newElement);

            // Add COCO-like annotation for each element
            let annotation = {
                id: index, // Unique ID for the annotation
                category_id: 1, // Assuming all elements are the same category
                bbox: [bbox.left, bbox.top, bbox.width, bbox.height],
                area: bbox.width * bbox.height,
                image_id: 1, // If you have multiple images, this needs to change accordingly
                iscrowd: 0
            };

            annotations.push(annotation);
        });
    });

    // Return annotations for further processing
    return annotations;
}


// Call markPage and get annotations
const annotations = markPage();
// console.log(annotations);

// If you need to pass the annotations back to Python, consider using a method like window.postMessage or an AJAX call to send data back to a server
// return annotations to python
// window.postMessage(annotations, "*");
