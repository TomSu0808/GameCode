Shader "Unlit/CharacterShader"
{
    Properties
    {
        [Header(Texture)]
            _MainTex("BaseTexture", 2D) = "white" {}
            _MaskTex("R: 高光强度  G: 边缘光强度  B:高光染色   A: 高光次幂 ", 2D) = "black"{}
            _NormalTex("NormalTexture", 2D) = "bump"{}
            _MatelnessMask("Metelness", 2D) = "black"{}
            _EmissionMask("EmissionTexture", 2D) = "black"{}
            _DiffWarpTex("ColorWarp", 2D) = "gray" {}
            _FresWarpTex("FresnelWarp", 2D) = "gray"{}
            _CubeMap("CubeMap", cube) = "_Skybox"{}
        [Header(lighting)]
            _LightColor("Light Color", color) = (1, 1, 1, 1)
            _MainColor("Main Color", color) = (1, 1, 1 ,1)
            _SpecPow("SpecPow", Range(0, 30)) = 5
            _SpecInt("SpecInt", Range(0, 30)) = 5
             _EnvCol("EnvCol", color) = (1, 1, 1 ,1)
             _EnvDiffInt("EnvDiffInt", Range(0.0, 5.0)) = 0.5
            _EnvSpecInt("环境镜面反射强度", Range(0.0, 10.0)) = 0.5
            _RimCol("RimColor", color) = (1, 1, 1, 1)
            _RimInt("RimLightInt", Range(0.0, 3.0)) = 1.0
           _EmissionInt ("Emission", Range(0.0, 10)) = 1.0
        [HideInInspector]
            _CutOff ("Alpha cutoff", Range(0, 1)) = 0.5
            _Color ("Main Color", Color) = (1, 1, 1 ,1)


    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            Name "FORWARD"
            Tags {
                "LightingMode" = "ForwardBase"
            }
                Cull Off
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #pragma multi_compile_fwdbase_fullshadows
            #pragma target 3.0
            #include "AutoLight.cginc"
            #include "Lighting.cginc"
            
            //texture
            uniform sampler2D _MainTex;
            uniform sampler2D _NormalTex;
            uniform sampler2D _MaskTex;
            uniform sampler2D _MatelnessMask;
            uniform sampler2D _EmissionMask;
            uniform sampler2D _DiffWarpTex;
            uniform sampler2D _FresWarpTex;
            uniform samplerCUBE _CubeMap;
            //Lighting
            uniform float3 _MainColor;
            uniform half _SpecPow;
            uniform half _SpecInt;
            uniform float _FresnelPow;
            uniform float _EmitInt;
            uniform half3 _LightColor;
            uniform half3 _EnvCol;
            uniform half3 _EnvDiffInt;
            uniform half _EnvSpecInt;
            uniform half3 _RimCol;
            uniform half _RimInt;
            uniform half _EmissionInt;
            uniform half _CutOff;
            uniform half3 _Color;

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv0 : TEXCOORD0;
                float4 normal : NORMAL;
                float4 tangent : TANGENT;

            };

            struct v2f
            {
                float2 uv0 : TEXCOORD0;
                float3 worldPos: TEXCOORD1;
                float4 pos : SV_POSITION;
                float3 worldNormal : TEXCOORD2;
                float3 worldTangent : TEXCOORD3;
                float3 worldBiTangent : TEXCOORD4;
                LIGHTING_COORDS(5,6)
            };

            float4 _MainTex_ST;

            v2f vert (appdata v)
            {
                v2f o;
                o.uv0 = v.uv0;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv0 = TRANSFORM_TEX(v.uv0, _MainTex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldTangent = normalize(mul(unity_ObjectToWorld, float4(v.tangent.xyz, 0.0)).xyz);
                o.worldBiTangent = normalize(cross(o.worldNormal, o.worldTangent) * v.tangent.w);

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                //vector
                float3 nDirTS = UnpackNormal(tex2D(_NormalTex, i.uv0)).rgb;//法线贴图数据

                float3x3 TBN = half3x3(i.worldTangent, i.worldBiTangent, i.worldNormal);
                float3 nDirWS = normalize(mul(nDirTS, TBN));

                float3 vDirWS = normalize(_WorldSpaceCameraPos.xyz - i.worldPos.xyz);
                float3 vrDirWS = reflect(-vDirWS, nDirWS);

                float3 lDirWS = normalize(_WorldSpaceLightPos0.xyz); //世界光
                float3 lrDirWS = reflect(-lDirWS, nDirWS);//反射方向R
                 //dot
                float ndotl = dot(nDirWS, lDirWS);
                float vdotr = dot(vDirWS, lrDirWS);
                float vdotn = dot(vDirWS, nDirWS);    ///////上面是没问题的，全是标准公式
                //采样纹理
                float4 var_MainTex = tex2D(_MainTex, i.uv0);
                float4 var_MaskTex = tex2D(_MaskTex, i.uv0);
                float4 var_MatelnessMask = tex2D(_MatelnessMask, i.uv0).r;
                float3 var_EmissionMask = tex2D(_EmissionMask, i.uv0).r;
                half3 var_FresWarpTex = tex2D(_FresWarpTex, i.uv0).rgb;
                half3 var_CubeMap = texCUBElod(_CubeMap, float4(vrDirWS, lerp(8.0, 0.0, var_MaskTex.a))).rgb;

                //提取信息
                float3 baseColor = var_MainTex.rgb;
                half opacity = var_MainTex.a;
                half specInt = var_MaskTex.r;
                half rimInt = var_MaskTex.g;
                half specTint = var_MaskTex.b;
                half specPow = var_MaskTex.a;
                half matellic = var_MatelnessMask;
                half emitInt = var_EmissionMask;
                half3 envCube = var_CubeMap;
                float shadow = LIGHT_ATTENUATION(i);

                //Lighting Model
                half3 diffCol = lerp(baseColor, half3(0.0, 0.0, 0.0), matellic);
                half3 specCol = lerp(baseColor, half3(0.3, 0.3, 0.3), specTint) * specInt;
                //Fresnel
                half3 fresnel = lerp(var_FresWarpTex, 0.0, matellic);
                half fresneCol = fresnel.r;
                half fresnelRim = fresnel.g;
                half fresnelSpec = fresnel.b;

                // light diffuse
                half halfLambert = ndotl * 0.5 + 0.5;
                half3 var_DiffWarpTex = tex2D(_DiffWarpTex, half2(halfLambert, 0.2));
                half3 dirDiff = diffCol * var_DiffWarpTex * _LightColor;

                // 光源镜面反射
                half phong = pow(max(0.0, vdotr), specPow * _SpecPow);
                half spec = phong * max(0.0, ndotl);
                 spec = max(spec, fresnelSpec);
                 spec = spec * _SpecInt;
                half3 dirSpec = specCol * spec * _LightColor;

                //环境漫反射
                half3 envDiff = diffCol * _EnvCol * _EnvDiffInt;
                //环境镜面反射
                half reflectInt = max(fresnelSpec, matellic) * specInt;
                half3 envSpec = specCol * reflectInt * envCube * _EnvSpecInt;

                //Rim Light
                half rimLight = _RimCol * fresnelRim * rimInt * max(0.0, nDirWS.g) * _RimInt;
                //Emission light
                half3 emission = diffCol * emitInt * _EmissionInt;

                //Final
                half3 finalRGB = (dirDiff + dirSpec) * shadow + envDiff + envSpec + rimLight + emission;

                //透明剪辑
                clip(opacity - _CutOff);

                return float4(finalRGB.rgb, 1.0);
            }
            ENDCG
        }
    }
    FallBack "Legacy Shader/Transparent/Cutout/VertexLit"
}
