
def parse_vcf(filename):
    contacts_with_birthdays = []
    with open(filename) as f:
        content = f.read()

        contacts = content.split('END:VCARD')

        bday_str = 'BDAY;VALUE=date:'

        for contact in contacts:
            if bday_str in contact:

                ind0 = contact.index('FN:')
                ind1 = contact.index('\n', ind0)
                name = contact[ind0 + len('FN:') : ind1]

                ind0 = contact.index(bday_str)
                ind1 = contact.index('\n', ind0)
                birthday = contact[ind0 + len(bday_str) : ind1].replace('-','')

                contacts_with_birthdays.append([name, birthday])

    return contacts_with_birthdays

def write_ics(contacts):
    with open("birthday_output_calendar.ics", "w") as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Posteo Webmail//NONSGML Calendar//EN\nX-WR-Timezone: Europe/London\n")
        for contact in contacts:
            f.write(f"BEGIN:VEVENT\nDTSTART:{contact[1]}T100000Z\nDTEND:{contact[1]}T110000Z\nRRULE:FREQ=YEARLY;UNTIL=20371231T230000Z;INTERVAL=1\nDTSTAMP:{contact[1]}T133638Z\nSEQUENCE:1754832998\nSUMMARY:Birthday: {contact[0]}\nCATEGORIES:None\nEND:VEVENT\n")
        f.write("END:VCALENDAR")

contacts_with_birthdays = parse_vcf("contacts.vcf")
print(f'found {len(contacts_with_birthdays)} contacts with birthdays')
write_ics(contacts_with_birthdays)