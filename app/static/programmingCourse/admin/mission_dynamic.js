(function waitForJQuery() {
    if (typeof django !== 'undefined' && django.jQuery) {
        const $ = django.jQuery;

        $(document).ready(function () {
            console.log("✅ Mission dynamic JS loaded");

            function updateMissionFields() {
                const type = $('#id_type').val();

                const choicesRow = $('#id_choices').closest('.form-row, .form-group');
                const evalPatternRow = $('#id_evaluation_pattern').closest('.form-row, .form-group');
                const answerRow = $('#id_answer').closest('.form-row, .form-group');

                const choicesInput = $('#id_choices');
                const evalInput = $('#id_evaluation_pattern');
                const answerInput = $('#id_answer');

                // Reset all placeholders
                choicesInput.attr('placeholder', '');
                evalInput.attr('placeholder', '');
                answerInput.attr('placeholder', '');

                if (type === 'code') {
                    choicesRow.hide();
                    evalPatternRow.show();
                    answerRow.hide();

                    evalInput.attr('placeholder', 'e.g. ^[a-zA-Z_][a-zA-Z0-9_]*\\s*=\\s*10$');
                    answerInput.attr('placeholder', 'Not used for code missions (can be left blank)');
                } else if (type === 'multiple_choice') {
                    choicesRow.show();
                    evalPatternRow.hide();
                    answerRow.show();

                    choicesInput.attr('placeholder', '["Option 1", "Option 2", "Option 3"]');
                    answerInput.attr('placeholder', 'One of the choices exactly: Option 1');
                } else if (type === 'true_false') {
                    choicesRow.hide();
                    evalPatternRow.hide();
                    answerRow.show();

                    answerInput.attr('placeholder', 'True or False');
                } else if (type === 'ordering') {
                    choicesRow.show();
                    evalPatternRow.hide();
                    answerRow.show();

                    choicesInput.attr('placeholder', '["Step A", "Step B", "Step C"]');
                    answerInput.attr('placeholder', 'Steps in order, comma-separated: Step A,Step B,Step C');
                } else {
                    // Default: show all
                    choicesRow.show();
                    evalPatternRow.show();
                    answerRow.show();
                }
            }

            $('#id_type').on('change', updateMissionFields);
            updateMissionFields(); // Run once on page load
        });
    } else {
        console.log("⏳ Waiting for django.jQuery...");
        setTimeout(waitForJQuery, 100);
    }
})();
