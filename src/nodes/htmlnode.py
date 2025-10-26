from src.nodes.textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf nodes must have a value")
        elif self.tag is None:
            return str(self.value)
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("parent nodes must have children")
        return f"<{self.tag}{super().props_to_html()}>" + "".join(child.to_html() for child in self.children) + f"</{self.tag}>"
        
