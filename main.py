import uuid

calendar_header = '''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example//NONSGML Calendar//EN
X-WR-Timezone: Europe/London\n'''

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
    with open("output_example.ics", "w") as f:
        f.write(calendar_header)
        for contact in contacts:
            f.write(f'''BEGIN:VEVENT
DTSTART:{contact[1]}T100000Z
DTEND:{contact[1]}T110000Z
RRULE:FREQ=YEARLY;UNTIL=20371231T230000Z;INTERVAL=1
DTSTAMP:{contact[1]}T133638Z
SEQUENCE:1754832998
SUMMARY:Birthday: {contact[0]}
CATEGORIES:None
UID:{str(uuid.uuid4())}
BEGIN:VALARM
ACTION:DISPLAY
SUMMARY:Birthday: {contact[0]}
TRIGGER:-P0DT1800S
END:VALARM
END:VEVENT\n''')
        f.write("END:VCALENDAR")

if __name__ == "__main__":
    contacts_with_birthdays = parse_vcf("input_example.vcf")
    print(f'found {len(contacts_with_birthdays)} contacts with birthdays')
    write_ics(contacts_with_birthdays)