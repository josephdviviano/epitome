#how to rsync files of a particular suffix across a network

rsync -PRav -e ssh --include '*.ghz' --include '*/' --exclude '*' B/. A/.


rsync -PRav -e ssh --include '*.1D' --include '*/' --exclude '*' SAB1/. /media/35B0-5E7F/export/.
