prompt = {"Numero1", "Numero2"};
nums = inputdlg(prompt, "Sumadora");

msgbox(sprintf("%d", str2num(nums{1}) + str2num(nums{2}) ), 'Suma');