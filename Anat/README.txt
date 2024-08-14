Before preparation step:
- SEt the range between 240-240 new value: 242
- Click on grow region
- Put to zero everything that is not 242
- Click on smooth a three times
- Then click on prepare

If SMP doesn t work then check:
- Go to mesh > Spatial TRansf : project to the VMR the mesh

Regulatization with morphoogical operation in BV
- Dilate twice
- Make everything 100
- Gaussian smooth
- Put to 240 everyhtong between 50-100
- Erode twice
- Smooth again a couple of times

hMT definition on the surface
Try to match the area that Marian had in the past
- sampling step: 0-3 step: 0.5; sample only positive + sample maximum value (see screenshot)
- Chang the colomap: default_pre-v21.olt
- Threshold 2,7
We can also smooth and then detect the biggest cluster
- Unthreshold map
- Smooth SMP few times
- Threshold again

V1, V2, V3 definition on the surface
When opening the sphere (same for all subjects, remember to check which file is linked in Mesh Morphing > ...LH_RECO_D160k_HIRES_SPH.srf)
Sampling ste: 0-2 mm, step: 0.5
Use Marian pg.186 for guidance
Remember to add the capsule that includes V1,V2,V3 and hMT
Usually, going back to the volume SMP -> VOI (0-5mm)
