---

title: Auto PBR Mapper Readme
lang: zh-tw
description: Auto PBR Mapper Readme
tags: RD, Blender, Addon

---

# AutoPBRMapper

Auto PBR Mapper

## Description

> addon for blender 2.8  
auto assign material with suffix mamed texture maps.

## Update

+ 20220210:  
  + add emission,height,displace map slot  
  + add exr format support  
  + shader type Mix/Principle, use opacity map for glass or leaves  
  + more clean shader tree nodes
  + reset material for file if objects lose material
  + texture convert tool  
  + a lot code refine for clear read

+ 20210810:  
  + fix glass/opacity realtime display problem due to eevee changed  
  + add opacity map invert node for quick fix different asset workflow  
  + more clear material tree  

+ 20210803:  
  + fix pbr path error when use folder select button  
  + fix non opacity shader's alpha blend mode  
  + fix gltf shader function broken  

+ 20210630:  
  + re assign material now more clearly to use .

+ 20210608:  
  + re-write struct and add re assign map for abc import.  
  + fix upper case alpha-numeric prefix error.  

## Todolist

+ [x] gltf material template
+ [ ] multi folder check
