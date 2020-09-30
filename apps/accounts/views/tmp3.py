# -*- coding: utf-8 -*-

# form holder
form_holder = {
    'majeur': {
        'class': FormClass1,
    },
    'majsoft': {
        'class': FormClass2,
    },
    'tiers1': {
        'class': FormClass3,
    },
    'tiers2': {
        'class': FormClass4,
    },
    'tiers3': {
        'class': FormClass5,
    },
    'tiers4': {
        'class': FormClass6,
    },
}

for key in form_holder.keys():
    # If the key is the same as the formlabel, we should use the posted data
    if request.POST.get('formlabel', None) == key:
        # Get the form and initate it with the sent data
        form = form_holder.get(key).get('class')(
            data=request.POST
        )

        # Validate the form
        if form.is_valid():
            # Correct data entries
            messages.info(request, _(u"Configuration validée."))

            if form.save():
                # Save succeeded
                messages.success(
                    request,
                    _(u"Données enregistrées avec succès.")
                )
            else:
                # Save failed
                messages.warning(
                    request,
                    _(u"Un problème est survenu pendant l'enregistrement "
                      u"des données, merci de réessayer plus tard.")
                )
        else:
            # Form is not valid, show feedback to the user
            messages.error(
                request,
                _(u"Merci de corriger les erreurs suivantes.")
            )
    else:
        # Just initiate the form without data
        form = form_holder.get(key).get('class')(key)()

    # Add the attribute for the name
    setattr(form, 'formlabel', key)

    # Append it to the tempalte variable that will hold all the forms
    forms.append(form)
