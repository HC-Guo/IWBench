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
        .filter(function (element) {
            // 过滤条件，比如元素可见性等
            var style = window.getComputedStyle(element);
            return style.display !== 'none' && style.visibility !== 'hidden' && element.offsetWidth > 0 && element.offsetHeight > 0;
        })
        .map(function (element) {
            // Get the bounding box for the entire element
            var bb = element.getBoundingClientRect();
            const rect = {
                left: Math.max(0, bb.left - bodyRect.left),
                top: Math.max(0, bb.top - bodyRect.top),
                width: bb.width,
                height: bb.height
            };

            return {
                element: element,
                rect: rect, // Single rectangle for the whole element
                text: element.textContent.trim().replace(/\s{2,}/g, ' ')
            };
        });


    // items = items.filter(x => !items.some(y => x.element.contains(y.element) && !(x === y)));

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

    items.forEach(function (item, index) {
        // Directly use the rect property of the item
        var bbox = item.rect;
    
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
            id: index,
            bbox: [bbox.left, bbox.top, bbox.width, bbox.height],
            area: bbox.width * bbox.height,
            element_type: item.element.tagName, // 元素类型，如 DIV, BUTTON 等
            class: item.element.className, // 类名
            id_attr: item.element.id, // ID 属性
        };

        annotations.push(annotation);
    });
    return annotations;
}

() => {
    const annotations = markPage();
    return annotations;
}

