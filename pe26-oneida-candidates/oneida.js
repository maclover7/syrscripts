const { readFile } = require('fs/promises');

const groupBy = (xs, func) => {
  return xs.reduce((acc, x) => {
    (acc[func(x)] = acc[func(x)] || []).push(x);
    return acc;
  }, {});
};

const partyLabels = {
  '"CON"': 'Conservative',
  '"DEM"': 'Democratic',
  '"REP"': 'Republican'
};

const toTitleCase = (str) => str.replace(
  /(\w)(\w*)/g,
  (_, firstChar, rest) => firstChar + rest.toLowerCase());

readFile('PE26_ONEIDA COUNTY BOE_CandidateStandardReport.csv')
.then(f => f.toString())
.then((f) => f.split("\n").map(r => r.split(",")).slice(1))
.then((rows) => groupBy(rows, r => r[0]))
.then((offices) => {
  return Object.keys(offices).map((office) => {
    const firstOfficeCandidate = offices[office][0];
    const officeName = firstOfficeCandidate[14].replace(' Member', '').replaceAll('"', '');
    const officeJurisdiction = toTitleCase(firstOfficeCandidate[13].split(' COUNTY COMMITTEE')[0]).replaceAll('"', '');
    const contestTitle = `${officeName} -- ${officeJurisdiction} (${partyLabels[firstOfficeCandidate[2]]})`;

    const officeCandidates = offices[office].map((candidate) => {
      return toTitleCase(candidate[15].replaceAll('"', ''));
    });

    console.log(contestTitle);
    officeCandidates.forEach(c => console.log(c));
  });
});