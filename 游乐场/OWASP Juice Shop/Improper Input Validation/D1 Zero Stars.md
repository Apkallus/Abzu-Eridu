- Zero Stars
    - 描述：给这家店一个毁灭性的零星评价。
    - 使用侧边栏的 Customer Feedback 功能
        - 其中控制评价的 HTML为
            ```html
            <input _ngcontent-ng-c4118930637="" type="range" matsliderthumb="" class="mdc-slider__input ng-valid ng-dirty ng-touched" aria-valuetext="1★" style="padding: 0px 16px; width: calc(100% + 10px); left: -21px;" step="1" min="1" max="5">
            ```
        - 修改属性值为 ```min="0"``` 并选择后提交按钮失效
        - 从按钮 HTML 中删除
            - ```class``` 值 ```mat-mdc-button-disabled```
            - ```disabled="true"```
        - 点击按钮提交评价
